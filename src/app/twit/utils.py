import tweepy
from django.conf import settings


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

	def daemon_runner(self):
		# exit on status_code in [420, 429] or ctrl C
		pass


class TwitSearch(object):

	def __init__(self):
		# init tweepy auth
		auth = tweepy.AppAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
		self.api = tweepy.API(auth)

	def search(self, keyswords):
		pass
