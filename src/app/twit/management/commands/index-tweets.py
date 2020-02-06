import lucene
from django.core.management.base import BaseCommand
from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client
from pymongo.cursor import Cursor


class Command(BaseCommand):
    help = "This will index all the tweets from mongodb. index sequentially [index hashtag, index tweets]"

    def handle(self, *args, **kwargs):

        try:
            # start lucene
            lucene.initVM()
        except:
            print('cant start the lucene VM')


        try:
            mongo_db = GetMongo_client()
        except:
            print('cant get mongo client')
            return

        for index_name in ['tweet_index', 'tag_index']:

            # get a fresh cursor for each worker
            mongo_db_cursor = mongo_db.twit_tweet.find()

            if isinstance(mongo_db_cursor, Cursor):
                worker = IndexManager()
                if index_name == 'tweet_index':
                    # delete the index to inorder to reindex
                    worker.remove_index(index_name)
                    worker.open_index(index_name)
                    worker.index_tweets(mongo_db_cursor)
                else:
                    # delete the index to inorder to reindex
                    worker.remove_index(index_name)
                    worker.open_index(index_name)
                    worker.index_hashtags(mongo_db_cursor)

                worker.close_index()
            else:
                print('cant connect to mongo')
        print('done')
