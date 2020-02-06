import tweepy
from progressbar import bar
from django.conf import settings
from pymongo import MongoClient
from dateutil import parser
import json
from bson.objectid import ObjectId


def GetMongo_client(collection_name='django'):
    client = MongoClient(settings.MONGO_URI)
    db = client['%s' % collection_name]
    return db


def loadJsonInMongo(filepath='%s/%s' %(settings.STORAGE_DIR, 'twit_tweet-standard.json')):
    db = GetMongo_client()
    # not to self use standard export feature from mongo
    # it export lines of json data
    with open(filepath) as f:
        for line in f:
            try:
                data = json.loads(line)

                if data.get('_id'):
                    _id = data.get('_id')
                    if _id.get('$oid'):
                        data['_id'] = ObjectId(data['_id']['$oid'])
                    # dupes are ignored
                db.twit_tweet.insert_one(data)
            except:
                pass

    # df = pd.read_json(filePath, orient='columns')
    # records_ = df
    # print(records_[0])
    # return
    # db.twit_tweet.remove()
    # result = db.twit_tweet.insert_many(data)
    print('total_record added', db.twit_tweet.count())


class TwitStreamListener(tweepy.StreamListener):
    def __init__(self, tweet_limit):
        self.db = GetMongo_client()
        self.tweet_limit = tweet_limit + self.db.command('collstats', 'twit_tweet')['size']
        self.progress_bar = bar.ProgressBar(max_value=self.tweet_limit)

    def on_connect(self):
        print("Connection established!!")
        self.progress_bar.start()

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_data(self, data):
        try:

            size = self.db.command('collstats', 'twit_tweet')['size']
            if size < self.tweet_limit:
                # process data here
                all_data = json.loads(data)
                if 'created_at' in all_data and all_data['lang'] == 'en':
                    if all_data['coordinates'] is not None or len(all_data['entities']['hashtags']) > 0:
                        all_data['created_at'] = parser.parse(all_data['created_at'])
                        self.db.twit_tweet.insert_one(all_data)
                        size = self.db.command('collstats', 'twit_tweet')['size']
                        self.progress_bar.update(size if size <= self.tweet_limit else self.tweet_limit)
            else:
                self.progress_bar.finish()
                # stop the streamer when progess is done
                return False
        except Exception as e:
            print(str(e))

    def on_error(self, status_code):
        if status_code in [420, 429]:
            # returning False in on_error disconnects the stream
            return False


class TwitStreamer(object):
    """
    The object to get all tweets from the stream

    """
    def __init__(self, total_tweets_size, creds):
        """
        Construct a new 'TwitStreamer' object.

        :param total_tweets_size: The size of data to be captured in bytes. To collect 5GB \
        data, set it to 1024*1024*1024*5. The actual data size may be slightly larger
        """
        # assert isinstance(total_tweets_size, int)
        assert isinstance(creds, dict)

        auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        self.Stream = tweepy.Stream(auth, listener=TwitStreamListener(total_tweets_size))

    def start(self):
        """
        Start stream capture and store tweets to MongoDB
        """
        # streamer docs
        # https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
        self.Stream.sample()

    def start_track(self, track_list):
        """
        Start stream capture and store tweets to MongoDB
        """
        # streamer docs
        # https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
        self.Stream.filter(languages=['en'], track=track_list)
