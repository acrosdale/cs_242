import lucene
from django.core.management.base import BaseCommand
from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client
from pymongo.cursor import Cursor


class Command(BaseCommand):
    help = "This will index all the tweets from mongodb. launch two process [index hashtag, index tweets]"

    def handle(self, *args, **kwargs):

        # start lucene
        lucene.initVM()
        running_processes = list()
        try:
            mongo_db = GetMongo_client()
            mongo_db_cursor = mongo_db.twit_tweet.find()
        except:
            mongo_db_cursor = None

        for index_name in ['tweet_index', 'tag_index']:

            if isinstance(mongo_db_cursor, Cursor):
                if index_name == 'tweet_index':
                    worker = IndexManager()
                    # delete the index to inorder to reindex
                    worker.remove_index(index_name)
                    worker.open_index(index_name)
                    worker.index_tweets(mongo_db_cursor)
                else:
                    worker = IndexManager()
                    # delete the index to inorder to reindex
                    worker.remove_index(index_name)
                    worker.open_index(index_name)
                    worker.index_hashtags(mongo_db_cursor)

        print('done')
