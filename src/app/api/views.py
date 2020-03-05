import os
import json
from lupyne import engine
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client
from bson.objectid import ObjectId


class TestApi(APIView):
	help = 'this api will enable user to search the tweet param of the tweet index'

	def get(self, request):
		param = 'johncena'
		response = Response(data={'goto for mongodb': "http://localhost:8081/db/django/twit_tweet"})

		# lucene.initVM() is init in the background
		# in shell make sure to call lucene.initVM()

		path = os.path.join(settings.STORAGE_DIR, 'tweet_index')

		if os.path.exists(path):
			index = IndexManager()

			# type of index ['tweet_index', 'tag_index']
			index.open_index('tweet_index')

			if index.indexer:
				hits = index.indexer.search('tweet:%s' % param)
				hit = hits[0].dict()
				id_str = hit['docid']

				db = GetMongo_client()

				query_data = db.twit_tweet.find_one({'_id': ObjectId(id_str)})

				if query_data:
					response.data['first_match_tweet'] = query_data.get('text')
					response.data['first_match_tweet_id'] = id_str
					response.data['total_match_tweet'] = hits.count

				index.close_index()

		return response


class SearchLuceneTweets(APIView):
	help = 'this api will enable user to search the tweet param of the tweet index'

	def get(self, request):

		query = request.GET.get('query', None)
		response = Response(data={})
		if query is None:
			return response

		q_obj = engine.Query
		q_list = list()

		# split on spaces
		query_components = query.split()

		# build query obj
		for field in ['tweet', 'descrpt', 'screen_name']:
			q_list.append(q_obj.term(field, query))

			if len(query_components) > 1:
				for comp in query_components:
					# do or OP
					q_list.append(q_obj.term(field, comp))
		# join queries
		is_first = True
		q_merged = None
		for q in q_list:
			if is_first:
				q_merged = q
				is_first = False
			else:
				q_merged |= q

		# open tweet index
		path = os.path.join(settings.STORAGE_DIR, 'tweet_index')
		if os.path.exists(path):
			index = IndexManager()
			index.open_index('tweet_index')
			if index.indexer:
				hits = index.indexer.search(q_merged)

				docids = list()
				# build return data
				# todo get top k match and sort by rank for lookup
				for hit in hits:
					docids.append(ObjectId(hit.dict()['docid']))

				# query data
				db = GetMongo_client()
				query_data = db.twit_tweet.find(
					{'_id': {'$in': docids}},
					{'_id': False, 'user.screen_name': True, 'text': True,  'coordinates': True}
				)
				response.data['bit_ops'] = str(q_list)
				response.data['query'] = str(q_merged)
				# we limit as the result can be too much
				response.data['results'] = list(query_data)

			index.close_index()
		return response


class SearchLuceneTags(APIView):
	help = 'this api will enable user to search the tweet param of the tag index'

	def get(self, request):
		# self.indexer.set('docid', stored=True)
		# self.indexer.set('rank', dimensions=1,stored=True)
		# self.indexer.set('tweet', engine.Field.Text)
		# self.indexer.set('rank', engine.Field.Text)
		# self.indexer.set('descrpt', engine.Field.Text)
		# self.indexer.set('coord', engine.SpatialField)
		# self.indexer.set('screen_name', engine.Field.Text)
		# self.indexer.set('date', engine.DateTimeField)
		# self.indexer.fields['loctn'] = engine.NestedField('state.city')
		pass

		# get param category and value
		# split query in it boolean part for query


class SearchHadoopIndex(APIView):
	help = 'this api will enable user to search the tweet param of the  hadoop inverted index'

	def get(self, request):
		param = 'johncena'
		response = Response(data={})



# >>> ind.indexer.search(q).count
# 1008
# >>> q =engine.Query.ranges('date',[1.4778368E9 ,1.5005151999999998E9])
# >>> ind.indexer.search(q).count
# 0
# >>>
# >>>
# >>>
# >>> d2 = datetime.date(2020, 2, 1)
# >>> d = datetime.date(2020, 1, 1)
# >>> q=engine.DateTimeField('date').range(d,d2)
# >>> ind.indexer.search(q).count
# 0
# >>> ind.close_index()
# True
# >>> ind.open_index('tweet_index')
# >>> ind.indexer.search(q).count
# 1
# >>> hits =ind.indexer.search(q)
# >>> hits
# <lupyne.engine.documents.Hits object at 0x7f6b0d7e39d0>
# >>> hits.dict()
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# AttributeError: 'Hits' object has no attribute 'dict'
# >>> hits[0].dict()