import tweepy
import math
import multiprocessing
from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand
from app.twit.utils import loadCSVInMongo


class Command(BaseCommand):
    help = "This will run tweepy and collect tweets via twitter API"
    run_default = True # this one run .sample()
    total_default = 1024*1024*1024*1  # 1 gig

    def add_arguments(self, parser):

        parser.add_argument(
            '-fp',
            '--filepath',
            type=str,
            help='where the load csv from. put csv in storage dir and use relative path'
        )

    def handle(self, *args, **kwargs):

        # retrieve args
        total_data = kwargs.get('filepath', None)
        print(total_data, 'HEREERRRRR')

