import os

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client


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

				query_data = db.twit_tweet.find_one({'id_str': id_str})

				if query_data:
					response.data['first_match_tweet'] = query_data.get('text')
					response.data['first_match_tweet_id'] = id_str
					response.data['total_match_tweet'] = hits.count

				index.close_index()

		return response


class SearchLuceneTweets(APIView):
	help = 'this api will enable user to search the tweet param of the tweet index'

	def get(self, request):

		response = Response(data={})


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