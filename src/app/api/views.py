import lucene
from rest_framework.views import APIView
from rest_framework.response import Response
from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client


class TestApi(APIView):
	help = 'this api will enable user to search the tweet param of the tweet index'

	def get(self, request):
		param = request.GET.get('param')
		response = Response(data={'goto for mongodb': "http://localhost:8081/db/django/twit_tweet"})

		# lucene.initVM() is init in the background
		# in shell make sure to call lucene.initVM()

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