from django.core.management.base import BaseCommand
import tweepy
import logging


class Command(BaseCommand):
	help = "This will run tweepy and collect tweets via twitter API"

	"https://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys"

	def handle(self, *args, **options):
		pass
