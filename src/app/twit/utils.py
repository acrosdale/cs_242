import tweepy
from progressbar import bar
from django.conf import settings
from pymongo import MongoClient
from dateutil import parser
import pandas as pd
import json


def GetMongo_client(collection_name='django'):
    a = 'mongodb://root:pleaseUseAStr0ngPassword@mongod:27017/admin'
    client = MongoClient(a)
    db = client['%s' % collection_name]

    # >> > db.twit_tweet
    # Collection(
    # 	Database(MongoClient(host=['mongod:27017'], document_class=dict, tz_aware=False, connect=True), 'django'),
    # 	'twit_tweet')
    # >> > db.list_collection_names()
    # ['__schema__', 'twit_tweet', 'django_migrations']

    return db


def loadCSVInMongo(filePath='twit/storage/data.csv'):
    db = GetMongo_client()
    df = pd.read_csv(filePath)
    records_ = json.loads(df.to_json(orient='records'))
    # print(records_)
    db.twit_tweet.remove()
    result = db.twit_tweet.insert_many(records_)
    print(db.twit_tweet.count())

class TwitStreamListener(tweepy.StreamListener):
    def __init__(self, tweet_limit):
        self.tweet_limit = tweet_limit
        self.progress_bar = bar.p(max_value=self.tweet_limit)

    def on_connect(self):
        print("Connection established!!")
        self.progress_bar.start()

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_data(self, data):
        db = GetMongo_client()
        size = db.command('collstats', 'twit_tweet')['size']
        if size < self.tweet_limit:
            # process data here
            all_data = json.loads(data)
            if 'created_at' in all_data and all_data['lang'] == 'en':
                if all_data['coordinates'] is not None or len(all_data['entities']['hashtags']) > 0 :
                    all_data['created_at'] = parser.parse(all_data['created_at'])
                    db.twit_tweet.insert_one(all_data)
                    size = db.command('collstats', 'twit_tweet')['size']
                    self.progress_bar.update(size if size <= self.tweet_limit else self.tweet_limit)
        else:
            self.progress_bar.finish()
            # this stop the streamer
            # return False

    def on_error(self, status_code):
        if status_code in [420, 429]:
            # returning False in on_error disconnects the stream
            return False


class TwitStreamer(object):
    """
    The object to get all tweets from the stream

    """
    def __init__(self,total_tweets_size):
        """
        Construct a new 'TwitStreamer' object.

        :param total_tweets_size: The size of data to be captured in bytes. To collect 5GB \
        data, set it to 1024*1024*1024*5. The actual data size may be slightly larger
        """
        isinstance(total_tweets_size, int)

        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
        self.Stream = tweepy.Stream(auth, listener=TwitStreamListener(total_tweets_size))

    def start(self):
        self.Stream.sample()
        """
        Start stream capture and store tweets to MongoDB
        """
    # streamer docs
    # https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

    def start(self, keywords):
        isinstance(keywords, list)
        assert len(keywords) > 0, 'keywords list is empty'
        # streamer docs
        # https://developer.twitter.com/en/docs/tweets/filteIndexManagerr-realtime/guides/basic-stream-parameters
        # self.Stream.filter(track=["car"])
        self.Stream.filter(languages=['en'], track=keywords)


# class TwitSearch(object):
#
# 	def __init__(self,keywords):
# 		# init tweepy auth
# 		auth = tweepy.AppAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
# 		self.api = tweepy.API(auth)
# 		self.keywords = keyswords
#
# 	def start(self):
# 		pass
