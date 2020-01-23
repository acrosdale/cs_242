from django.core.management.base import BaseCommand
from app.twit.utils import TwitStreamListener
import tweepy
import logging


class GetTwitterData(BaseCommand):
	help = "This will run tweepy and collect tweets via twitter API"

	"https://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys"

	"""
		save file : text, timestamp, geolocation, user of tweet, links, hashtag
	"""

	def handle(self, *args, **options):
		pass

	def twit_streaming(self):
		pass

	def twit_search(self):
		pass




"""
	twitter attribute
	
	created_at	: utc_String
	text		: String
	user		: user-obj
	coordinates	: coordinates-obj  OR/AND  place : place-obj
	
	entities 	: Entities obj <---HashTag are here
	"lang"		: "en"


"""
