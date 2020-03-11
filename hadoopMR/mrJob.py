from mrjob.job import MRJob
import re
from pymongo import MongoClient
import simplejson as json
import math
import random
import json


class BuildInvertedIndex(MRJob):
    def mapper(self, _, line):
        tweetid = line.split(",",1)[0]
        tweettext = line.split(",", 1)[1]
        # Add ranking function here :
        rank = random.randint(1, 21)
        tweetObj = {"tweetId": tweetid, "tweetText": tweettext, "rank": rank}

        for word in str(tweettext).split(" "):
            yield (word, tweetObj)

    def reducer(self, word, tweetTuples):
        yield (word, list(tweetTuples))


if __name__ == '__main__':
    BuildInvertedIndex.run()
