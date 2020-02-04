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
        #assume queryset_cursor is db variable, run db = GetMongo_client() out side
        # return as [(docid,[hashtag1,hashtag2....]),.......]
        indexer.set('docid', stored=True)#username
        indexer.set('hashtag', engine.Field.Text)
        #indexer.set('hashtag', stored=True)#tweet
        #indexer.set('text', engine.Field.Text)
        
        tweet=queryset_cursor.twit_tweet.find()
        list_of_tweet=list(queryset_cursor.twit_tweet.find())
        tuple_list=[]
        for obj in list_of_tweet:
            docid=obj['_id']
            hashtags=obj['entities']['hashtags']
            hash_list=[]
            for item in hashtags:
                hash_list.append(item['text'])
            tuple_list.append((docid,hash_list))
            
        return tuple_list
            
        #for item in tuple_list:
        #    indexer.add(docid=str(item[0]), hashtag=' '.join([ w,i for i,w in enumerate(item[1]) ]))
        #    indexer.commit()   

    def index_commit(self):
        assert self.indexer is not None, 'index is not found'
        self.indexer.commit()
