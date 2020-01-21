from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class TestApi(APIView):

	def get(self, request):

		response = Response(data={'msg': 'apis operational'})

		return  response

	# def get_queryset(self):
	# 	pass