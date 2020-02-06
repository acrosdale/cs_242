import lucene
from django.core.management.base import BaseCommand
from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client
from pymongo.cursor import Cursor
import multiprocessing


class Command(BaseCommand):
    help = "This will index all the tweets from mongodb. index concurrently [index hashtag, index tweets]"

    def handle(self, *args, **kwargs):

        indexes = ['tweet_index', 'tag_index']
        running_processes = []
        for index in indexes:

            worker = Worker(index)
            process = multiprocessing.Process(target=worker.start)
            print("start build process of %s" % index)
            process.start()
            running_processes.append(process)

        for proc in running_processes:
            proc.join()

        print(*indexes, 'finish building..concurrently')


class Worker(object):
    def __init__(self, index_name):
        assert index_name in ['tweet_index', 'tag_index']
        self.index_name = index_name

    def start(self):
        print('WORKER FOR %s STARTED' % self.index_name)
        try:
            # start lucene
            lucene.initVM()
        except:
            print('cant start the lucene VM')

        try:
            mongo_db = GetMongo_client()
            mongo_db_cursor = mongo_db.twit_tweet.find()
        except:
            print('cant get mongo client')
            return

        if isinstance(mongo_db_cursor, Cursor):
            worker = IndexManager()
            worker.remove_index(self.index_name)
            worker.open_index(self.index_name)

            if self.index_name == 'tag_index':
                worker.index_hashtags(mongo_db_cursor)
            else:
                worker.index_tweets(mongo_db_cursor)

            worker.close_index()
            print('WORKER FOR %s finished' % self.index_name)
