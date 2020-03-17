from mrjob.job import MRJob
import re
from pymongo import MongoClient
import simplejson as json
import math
import random
import json
import os
import shutil
import datetime
import numpy as np

client = MongoClient(
    'mongodb://root:pleaseUseAStr0ngPassword@mongod:27017/admin')
collection_name = 'django'
db = client['%s' % collection_name]
collection = db['ranked_index']


def get_rank(self, tweetId):
    # assert isinstance(tweet, dict)

    twitCollection = db['twit_tweet']
    tweet = twitCollection.find_one({'id': int(tweetId)})
    user_dict = tweet.get('user', None)
    #print(user_dict)
    if not user_dict:
        return -(10**10)

    #time
    time = user_dict.get("created_at", None)
    if not time:
        score_time = 0
    else:
        time = time.split()[1:]
        state_counts = user_dict.get("statuses_count", 0)

        currentDT = datetime.datetime.now()
        currentDT = str(currentDT).split()
        y, m, d = currentDT[0].split('-')
        hour, mini, _ = currentDT[1].split(':')

        monthToNum = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }

        y = abs(int(time[-1]) - int(y))
        m = abs(monthToNum[time[0]] - int(m))
        d = abs(int(time[1]) - int(d))
        h = abs(int(time[2].split(":")[0]) - int(hour))
        mini = abs(int(time[2].split(":")[1]) - int(mini))
        if y * 12 * 30 * 24 * 60 + m * 30 * 24 * 60 + d * 24 * 60 + h * 60 + mini == 0:
            score_time = 10
        else:
            if state_counts == 0:
                score_time = -np.log10(y * 12 * 30 * 24 * 60 + m * 30 * 24 *
                                       60 + d * 24 * 60 + h * 60 + mini) * 1
            else:
                score_time = -np.log10(y * 12 * 30 * 24 * 60 +
                                       m * 30 * 24 * 60 + d * 24 * 60 +
                                       h * 60 + mini) * (1 - 1 / state_counts)

    #friendship connection
    followers_count = user_dict.get("followers_count", None)
    friends_count = user_dict.get("friends_count", None)
    if not followers_count or not friends_count or followers_count == 0:
        score_connection = 0
    else:
        diff_rate = followers_count - friends_count
        if diff_rate > 0:
            normalized_diff = len(str(diff_rate)) * int(str(diff_rate)[:1])
        elif diff_rate < 0:
            normalized_diff = -len(str(diff_rate)[1:]) * int(str(diff_rate)[1])
        else:
            normalized_diff = 1
            #interact=2*(friends_count*followers_count)/(followers_count+friends_count)
            #if diff_rate!=0:
        score_connection = np.log2(followers_count + 1) * (normalized_diff)

    #social verification
    protected = user_dict.get("protected", 'NULL')
    verified = user_dict.get("verified", 'NULL')
    favourites_count = user_dict.get("favourites_count", None)

    if protected == 'NULL':
        protected = 0
    if verified == 'NULL':
        verified = 0
    if not favourites_count:
        favourites_count = 0

    final_score = int(
        (score_connection + score_time + np.log2(favourites_count + 1) *
         (1 + protected + verified) + 6) * 100)  #one month shift, 10**6

    if final_score < 0:
        final_score = 0

    #print(final_score)
    return final_score


class BuildInvertedIndex(MRJob):
    def mapper(self, _, line):
        tweetid = line.split(",", 1)[0]
        tweettext = line.split(",", 1)[1]
        # Add ranking function here :
        # rank = random.randint(1, 2000)
        rank = get_rank(self, tweetid)
        tweetObj = {"tweetId": tweetid, "tweetText": tweettext, "rank": rank}

        for word in str(tweettext).split(" "):
            yield (word, tweetObj)

    def reducer(self, word, tweetTuples):
        collection.insert_one({"word": word, "tweets": list(tweetTuples)})
        # yield (word, list(tweetTuples))


if __name__ == '__main__':
    BuildInvertedIndex.run()