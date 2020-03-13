import os
import json
import datetime
from lupyne import engine
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from app.twit.indexer import IndexManager
from app.twit.utils import GetMongo_client
from bson.objectid import ObjectId
from app.twit.utils import merge_result


class TestApi(APIView):
	help = 'this api will enable user to search the tweet param of the tweet index'

	def get(self, request):
		param = 'Basketball'
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
				if hits.count:
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

		# split on spaces
		query_components = query.split()

		# open tweet index
		path = os.path.join(settings.STORAGE_DIR, 'tweet_index')
		if os.path.exists(path):
			tweet_index = IndexManager()
			try:
				tweet_index.open_index('tweet_index')
				if tweet_index.indexer:
					# build query obj
					res_id_rank = dict()
					for field in ['tweet']:
						if len(query_components):
							for _or in query_components:
								if _or:
									q = '%s:%s' % (field, _or)
									or_hits = tweet_index.indexer.search(q)
									for hit in or_hits:
										if not res_id_rank.get(hit['docid'], None):
											res_id_rank[hit['docid']] = hit['rank']

					id_rank = res_id_rank
					docids = list()
					# build return data
					# todo get top k match and sort by rank for lookup
					hits_list = sorted(id_rank.items(), key=lambda x: x[1], reverse=True)
					for hit_tuple in hits_list:
						docids.append(ObjectId(hit_tuple[0]))

					# query data
					db = GetMongo_client()
					query_data = db.twit_tweet.find(
						{'_id': {'$in': docids}},
						{'_id': True, 'user.screen_name': True, 'text': True, 'coordinates': True}
					)

					# sort relevance
					query_data = list(query_data)
					for data in query_data:
						data['rank'] = id_rank[str(data['_id'])]
						del data['_id']

					# SORTED BY RANK IE RELEVANCE
					query_data = sorted(query_data, key=lambda i: i['rank'], reverse=True)

					response.data['results'] = query_data
					response.data['total_results'] = len(query_data)
			except:
				response.data['results'] = []
			tweet_index.close_index()
		return response


class SearchLuceneTweetsAdvance(APIView):
	help = 'this api will enable user to search the tweet param of the tag index'

	def get(self, request):
		response = Response(data={})
		request.GET.get('query', None)

		# collect request data
		ands = request.GET.get('and', None)
		ors = request.GET.get('or', None)
		nots = request.GET.get('not', None)
		date_range = request.GET.get('date_range', None)
		city = request.GET.get('city', None)
		state = request.GET.get('state', None)
		hashtags = request.GET.get('hashtags', None)

		id_rank = dict()

		# indexes
		tweet_path = os.path.join(settings.STORAGE_DIR, 'tweet_index')
		tag_path = os.path.join(settings.STORAGE_DIR, 'tag_index')
		tag_index = None
		tweet_index = None
		try:
			if os.path.exists(tag_path):
				tag_index = IndexManager()
				tag_index.open_index('tag_index')

			if os.path.exists(tweet_path):
				tweet_index = IndexManager()
				tweet_index.open_index('tweet_index')

			if date_range:
				date_range = date_range.split('-')
				date_1 = date_range[0].split('/')
				date_2 = date_range[1].split('/')
				d2 = datetime.date(int(date_2[2]), int(date_2[0]), int(date_2[1]))
				d1 = datetime.date(int(date_1[2]), int(date_1[0]), int(date_1[1]))

				q = engine.DateTimeField('date').range(d1, d2)
				date_hits = tweet_index.indexer.search(q)

				for hit in date_hits:
					id_rank[hit['docid']] = hit['rank']
			if city and state:
				state_hits = tweet_index.indexer.search('state:%s' % state)
				city_hits = tweet_index.indexer.search('city:%s' % city)
				temp_id_rank = dict()
				res_id_rank = dict()

				for hit in city_hits:
					temp_id_rank[hit['docid']] = hit['rank']
				for hit in state_hits:
					if temp_id_rank.get(hit['docid'], None):
						res_id_rank[hit['docid']] = hit['rank']

				id_rank = merge_result(id_rank, res_id_rank)
			elif state:
				state_hits = tweet_index.indexer.search('state:%s' % state)
				res_id_rank = dict()
				for hit in state_hits:
					res_id_rank[hit['docid']] = hit['rank']

				id_rank = merge_result(id_rank, res_id_rank)
			if hashtags:
				hashtags = hashtags.split(',')
				tag_id_rank = dict()
				for hashtag in hashtags:
					if hashtag:
						tag_hits = tag_index.indexer.search('hashtag:%s' % hashtag)
						for hit in tag_hits:
							tag_id_rank[hit['docid']] = hit['rank']

				id_rank = merge_result(id_rank, tag_id_rank)
			if ors:
				ors = ors.split(',')
				res_id_rank = dict()
				for _or in ors:
					if _or:
						for field in ['tweet']:
							q = '%s:%s' % (field, _or)
							or_hits = tweet_index.indexer.search(q)
							for hit in or_hits:
								res_id_rank[hit['docid']] = hit['rank']
				id_rank = merge_result(id_rank, res_id_rank)
			if ands:
				ands = ands.split(',')
				interm_dict1 = dict()

				for field in ['tweet']:
					for _and in ands:
						q = '%s:%s' % (field, _and)
						and_hits = tweet_index.indexer.search(q)
						interm_dict2 = dict()
						for hit in and_hits:
							interm_dict2[hit['docid']] = hit['rank']

						if not len(interm_dict1):
							interm_dict1 = interm_dict2
						else:
							temp_dict = dict()
							for k, v in interm_dict2.items():
								if interm_dict1.get(k, None):
									temp_dict[k] = v
							interm_dict1 = temp_dict
				id_rank = merge_result(id_rank, interm_dict1)
			if nots:
				nots = nots.split(',')
				not_list = list()
				for _not in nots:
					if _not:
						for field in ['tweet']:
							q = '%s:%s' % (field, _not)
							or_hits = tweet_index.indexer.search(q)
							for hit in or_hits:
								not_list.append(hit['docid'])
				for k in not_list:
					if id_rank.get(k, None):
						del id_rank[k]
		except:
			if tweet_index:
				tweet_index.close_index()
			if tag_index:
				tag_index.close_index()
			response.data['results'] = []
			return response

		docids = list()
		# build return data
		# todo get top k match and sort by rank for lookup
		hits_list = sorted(id_rank.items(), key=lambda x: x[1], reverse=True)
		for hit_tuple in hits_list:
			docids.append(ObjectId(hit_tuple[0]))

		# query data
		db = GetMongo_client()
		query_data = db.twit_tweet.find(
			{'_id': {'$in': docids}},
			{'_id': True, 'user.screen_name': True, 'text': True, 'coordinates': True}
		)

		# sort relevance
		query_data = list(query_data)
		for data in query_data:
			data['rank'] = id_rank[str(data['_id'])]
			del data['_id']

		# query_data[15]['rank'] = 12.0

		# SORTED BY RANK IE RELEVANCE
		query_data = sorted(query_data, key=lambda i: i['rank'], reverse=True)

		response.data['results'] = query_data
		response.data['total_results'] = len(query_data)
		if tweet_index:
			tweet_index.close_index()
		if tag_index:
			tag_index.close_index()

		return response


class SearchHadoopIndex(APIView):
	help = 'this api will enable user to search the tweet param of the  hadoop inverted index'

	def get(self, request):
		param = 'johncena'
		response = Response(data={})
