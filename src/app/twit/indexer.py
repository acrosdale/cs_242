import lucene
from lupyne import engine
from django.conf import settings
# from twit.models import TwitUser


class IndexManager(object):
    def __init__(self):
        # https://pythonhosted.org/lupyne/examples.html
        #http://lupyne.surge.sh/
        # init pylucene
        # DO NOT REMOVE THIS!!
        try:
            lucene.initVM()
        except:
            self.indexer = None

        # closing is handled automatically
    def close_index(self):
        self.indexer = None
        return True

    def open_index(self, index_path='%s/%s' % (settings.STORAGE_DIR, 'index_test')):
        # create or open and index
        self.indexer = engine.Indexer(index_path)

    def index_tweets(self, queryset_cursor):
        assert self.indexer is not None, 'index is not found'
        # code to index the field in the tweets

        pass

    def index_hashtags(self, queryset_cursor):
        assert self.indexer != None
        # we need to index hastag seperately
        # note on hashtag the name will duplicates
        # so when searching retrieve id as a set()
        pass

    def index_commit(self):
        assert self.indexer is not None, 'index is not found'
        self.indexer.commit()
