import lucene
import os
from lupyne import engine
from django.conf import settings
from dateutil import parser
import shutil
import datetime
from geopy.geocoders import Nominatim

import re


# IMPORTANT always start the lucene.initVM() before USING THIS CLASS

class IndexManager(object):

    def __init__(self):
        # assert lucene.getVMEnv() or lucene.initVM()
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
            self.indexer.set('docid', stored=True)
            self.indexer.set('rank', dimensions=1, stored=True)
            self.indexer.set('hashtag', engine.Field.Text)
            self.indexer.fields['loctn'] = engine.NestedField('state.city')
            self.indexer.set('date', engine.DateTimeField)
        else:
            # create index
            self.indexer = engine.Indexer(path)

            # code to index the field in the tweets
            self.indexer.set('docid', stored=True)
            self.indexer.set('rank', dimensions=1, stored=True)
            self.indexer.set('tweet', engine.Field.Text)
            self.indexer.set('descrpt', engine.Field.Text)
            # this lat and long tuple
            self.indexer.set('coord', engine.SpatialField)
            self.indexer.set('screen_name', engine.Field.Text)
            self.indexer.fields['loctn'] = engine.NestedField('state.city')
            self.indexer.set('date', engine.DateTimeField)

    def get_rank(self, tweet):
        assert isinstance(tweet, dict)
        
        for obj,v_obj in tweet.items():
            user_dict=obj.get('user', None)
            for user_key,user_v user_dict.items():
                pass
            
        return 1.0

    def index_tweets(self, queryset_cursor):
        assert self.indexer is not None, 'index is not found'

        count = 0
        for obj in queryset_cursor:
            doc_id = str(obj.get('_id'))
            tweet = obj.get('text', None)
            date_created = obj.get('created_at')
            date_created = datetime.date(date_created.year, date_created.month, date_created.day)

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
                    print(coord[0], coord[1])
                    coord = [(float(coord[0]), float(coord[1]))]
                    count +=1

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
                    loctn=loctn,
                    date=date_created,
                    rank=self.get_rank(obj)
                )
            except Exception as e:
                print('error', str(e))

        self.index_commit()
        print(count)

    def index_hashtags(self, queryset_cursor,ngram=0):
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

            docid = str(obj.get('_id'))
            hashtags_obj = obj.get('entities', None)
            date_created = obj.get('created_at')
            date_created = datetime.date(date_created.year, date_created.month, date_created.day)

            # skip id no tag are found
            if not hashtags_obj:
                continue

            place_obj = obj.get('place', None)

            if place_obj:
                loctn = place_obj.get('full_name', None)

                if loctn and len(loctn.split(',')) == 2:
                    city, state = loctn.split(',')
                    state = state.strip()
                    loctn = state + '.' + city
            else:
                loctn = ''

            hashtags = hashtags_obj.get('hashtags')

            if hashtags and docid:
                for item in hashtags:
                    if item.get('text', None):
                        try:
                            if ngram > 1:
                                self.indexer.add(
                                   docid=docid,
                                   hashtag=self.char_ngram_preprocessing(list(item['text']), ngram)
                                )
                            else:
                                self.indexer.add(
                                    docid=docid,
                                    hashtag=item['text'],
                                    rank=self.get_rank(obj),
                                    date=date_created,
                                    loctn=loctn
                                )
                        except Exception as e:
                            print(str(e))

        self.index_commit()

    def index_commit(self):
        assert self.indexer is not None, 'index is not found'
        self.indexer.commit()

    # you dont need this. you most like access indexer wrong
    # based on the notes written in the report
    def char_ngram_preprocessing(self, word_list,ngram):
        final=''
        for i,char in enumerate(' '.join(word_list)):
            final+=word_list[i:i+ngram]

        return final


class QueryParser(object):
    def __init__(self):
        pass

    def is_date(self, query):
        assert isinstance(query, str), 'the query is not a string'
        pass

    def is_hastag(self, query):
        assert isinstance(query, str), 'the query is not a string'
        pass

    def is_tweet_term(self, query):
        assert isinstance(query, str), 'the query is not a string'
        pass

    def parse_query(self, query):
        assert isinstance(query, str), 'the query is not a string'
        pass


class IndexSearcher(object):
    def __init__(self, index_name=None):
        assert index_name in ['tweet_index', 'tag_index']

        if index_name:
            path = os.path.join(settings.STORAGE_DIR, index_name)
            backup_index = os.path.join(settings.BACKUP_DIR, index_name)

            if os.path.exists(path):
                self.indexer = IndexManager()
                self.indexer.open_index(index_name)

            elif os.path.exists(backup_index):
                self.indexer = IndexManager()
                self.indexer.open_index(index_name)

            else:
                raise AssertionError('index does not exist')
        else:
            self.indexer = None

        self.query_parser = QueryParser()

    def search_index(self, query):
        assert isinstance(query, str), 'the query is not a string'

        # is it a hashtag
        # is it a date
        # is a word or words
        pass



