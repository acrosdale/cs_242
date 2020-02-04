import tweepy
import math
import multiprocessing
from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand
from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client


class Command(BaseCommand):
    help = "This will index all the tweets from mongodb. launch two process [index hashtag, index tweets]"

    def handle(self, *args, **kwargs):

        pass
