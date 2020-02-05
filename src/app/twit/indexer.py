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
        indexer.set('usr_id', stored=True)
        indexer.set('tweet', stored=True)
        indexer.set('descrpt', stored=True)
        indexer.set('coord', stored=True)
        indexer.set('screen_name', stored=True)
        indexer.set('loctn', stored=True)

        list_of_tweet = list(queryset_cursor.twit_tweet.find())
        tuple_list = []
        for obj in list_of_tweet:
            user = obj['user']['id']
            tweet = obj['text']
            descrpt = obj['user']['description']
            coord = obj['coordinates']['coordinates']
            screenname = obj['user']['screen_name']
            loctn = obj['place']['country']
            tuple_list.append((user, tweet, descrpt, coord, screenname, loctn))
        for item in tuple_list:
            indexer.add(usr_id=item[0], tweet=item[1], descrpt=item[2], coord=item[3], screen_name=item[4], loctn= item[5])
            indexer.commit()

        return indexer
        

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
            
        #return tuple_list
            
        for item in tuple_list:
            indexer.add(docid=str(item[0]), hashtag=' '.join(item[1]))
        
        self.indexer=indexer

    def index_commit(self):
        assert self.indexer is not None, 'index is not found'
        self.indexer.commit()

    def char_ngram_preprocessing(self,word_list,ngram):
        final=''
        for i,char in enumerate(' '.join(word_list)):
            final+=word_list[i:i+ngram]
        
        return final
                
