from rest_framework.views import APIView
from rest_framework.response import Response
# from twit.models import Tweet
# from .serializers import TweetSerializer
# from dateutil import parser
# import pytz


# Create your views here.
class TestApi(APIView):

	def get(self, request):


		response = Response(data={'goto for mongodb': "http://localhost:8081/db/django/twit_tweet"})

		return response