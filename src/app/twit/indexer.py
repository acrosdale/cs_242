import lucene
import os
from lupyne import engine
from django.conf import settings
import shutil

import re


# IMPORTANT always start the lucene.initVM() before USING THIS CLASS

class IndexManager(object):

    def __init__(self):
        self.indexer = None
        # closing is handled automatically

    def close_index(self):
        self.indexer = None
        return True

    def remove_index(self, index_name):
        assert index_name in ['tweet_index', 'tag_index']
        self.indexer = None

        path = os.path.join(settings.STORAGE_DIR, index_name)

        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except:
               pass

    def open_index(self, index_name):
        assert index_name in ['tweet_index', 'tag_index']

        path = os.path.join(settings.STORAGE_DIR, index_name)

        if os.path.exists(path):
            # open index
            self.indexer = engine.Indexer(path)

        elif index_name == 'tag_index':
            # create index
            self.indexer = engine.Indexer(path)
            self.indexer.set('docid', stored=True)  # username
            self.indexer.set('hashtag', engine.Field.Text)
        else:
            # create index
            self.indexer = engine.Indexer(path)

            # code to index the field in the tweets
            self.indexer.set('docid', stored=True)
            self.indexer.set('tweet', engine.Field.Text)
            self.indexer.set('descrpt', engine.Field.Text)
            self.indexer.set('coord', engine.SpatialField)
            self.indexer.set('screen_name', engine.Field.Text)
            # self.indexer.set('loctn', engine.Field.Text)
            self.indexer.fields['loctn'] = engine.NestedField('state.city')

    def index_tweets(self, queryset_cursor):
        assert self.indexer is not None, 'index is not found'

        for obj in queryset_cursor:
            doc_id = str(obj.get('id'))
            tweet = obj.get('text', None)

            # removes emoji
            tweet = settings.EMOJI_PATTERN.sub('', tweet)

            user_dict = obj.get('user', None)
            coord_obj = obj.get('coordinates', None)
            place_obj = obj.get('place', None)

            if user_dict:
                descrpt = user_dict.get('description', None)
                screen_name = user_dict.get('screen_name', None)

                if not descrpt:
                    descrpt = ''

                if not screen_name:
                    screen_name = ''
            else:
                descrpt = ''
                screen_name = ''

            if coord_obj:
                coord = coord_obj.get('coordinates', None)
                if coord:
                    coord = [tuple(coord)]
            else:
                coord = []

            if place_obj:
                loctn = place_obj.get('full_name', None)

                if loctn and len(loctn.split(',')) == 2:
                    city, state = loctn.split(',')
                    state = state.strip()
                    loctn = state + '.' + city
            else:
                loctn = ''
            try:
                self.indexer.add(
                    docid=doc_id,
                    tweet=tweet,
                    descrpt=descrpt,
                    coord=coord,
                    screen_name=screen_name,
                    loctn=loctn
                )
            except Exception as e:
                print(str(e))

        self.index_commit()

    def index_hashtags(self, queryset_cursor):
        assert self.indexer is not None
        # we need to index hastag seperately
        # note on hashtag the name will duplicates
        # so when searching retrieve id as a set()
        # assume queryset_cursor is db variable, run db = GetMongo_client() out side
        # return as [(docid,[hashtag1,hashtag2....]),.......]
        # indexer.set('docid', stored=True)#username
        # indexer.set('hashtag', engine.Field.Text)
        # indexer.set('hashtag', stored=True)#tweet
        # indexer.set('text', engine.Field.Text)
        
        # tweet=queryset_cursor.twit_tweet.find()
        # list_of_tweet=list(queryset_cursor.twit_tweet.find())
        # tuple_list=[]
        for obj in queryset_cursor:

            docid = str(obj.get('id'))
            hashtags_obj = obj.get('entities')
            hashtags = hashtags_obj.get('hashtags')

            if hashtags and docid:
                for item in hashtags:
                    if item.get('text', None):
                        try:
                            self.indexer.add(
                                docid=docid,
                                hashtag=item['text']
                            )
                        except Exception as e:
                            print(str(e))

        self.index_commit()

    def index_commit(self):
        assert self.indexer is not None, 'index is not found'
        self.indexer.commit()

    def char_ngram_preprocessing(self, word_list,ngram):
        final=''
        for i,char in enumerate(' '.join(word_list)):
            final+=word_list[i:i+ngram]
        
        return final
