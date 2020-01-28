import tweepy
from django.conf import settings
from pymongo import MongoClient


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


class TwitStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		# integrate orm here to store on the model
		print(status.text)

	def on_error(self, status_code):
		if status_code in [420, 429]:
			# returning False in on_error disconnects the stream
			return False


class TwitStreamer(object):

	def __init__(self):

		# init tweepy auth
		auth = tweepy.AppAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
		api = tweepy.API(auth)

		# init twit stream
		self.Stream = tweepy.Stream(auth=api.auth, listener=TwitStreamListener())

	def start(self):
		# exit on status_code in [420, 429] or ctrl C
		pass


class TwitSearch(object):

	def __init__(self,keywords):
		# init tweepy auth
		auth = tweepy.AppAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
		self.api = tweepy.API(auth)
		self.keywords = keyswords

	def start(self):
		pass
