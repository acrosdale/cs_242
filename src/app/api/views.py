from rest_framework.views import APIView
from rest_framework.response import Response
from twit.models import Tweet, TwitUser
from .serializers import TweetSerializer
from dateutil import parser
import pytz


# Create your views here.
class TestApi(APIView):

	def get(self, request):

		sample = {
			'date_created': parser.parse('Wed Oct 10 20:19:24 +0000 2018').replace(tzinfo=pytz.utc),
			'text': 'blah',
			'coordinates': [-125.3156, 126.4538],
			'hashtags': ['ucr', 'Riverside'],
			'user': TwitUser(**{
				"user_id": 1,
				"name": 'group 20',
				"screen_name": '20-gang',
				"location": 'Riverside',
				"description": ' this is for a group project sample',
				"verified": True,
				"followers_count": 5,
				"friends_count": 100
			})
		}

		if Tweet.objects.exists():
			pass
		else:
			Tweet(**sample).save()

		# twit = Tweet.objects.get(id=1)
		#
		# # if twit.count() > 1:
		# # 	serial = TweetSerializer(twit, many=True)
		# # else:
		# # 	serial = TweetSerializer(twit)
		#
		# serial = TweetSerializer(twit)

		response = Response(data={'goto for mongodb': "http://localhost:8081/db/django/twit_tweet"})

		return response