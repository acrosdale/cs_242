import tweepy
import logging
import random
import multiprocessing

from django.core.management.base import BaseCommand
from django.db import connection

from app.twit.utils import TwitSearch, TwitStreamer


class GetTwitterData(BaseCommand):
	help = "This will run tweepy and collect tweets via twitter API"
	max_stream_processes = 1
	max_search_processes = 1

	"https://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys"

	"""
		save file : text, timestamp, geolocation, user of tweet, links, hashtag
	"""

	def handle(self, *args, **options):
		pass

		# print('Starting TWIT CMD')
		#
		#
		# running_processes = []
		# transfer_to_process = list(self.qs.values_list('id', flat=True))
		#
		# running_processes_cleared = False
		# while len(transfer_to_process) > 0 or not running_processes_cleared:
		# 	while len(running_processes) < self.max_processes and len(transfer_to_process) > 0:
		#
		# 		random_company_id = random.choice(transfer_to_process)
		# 		transfer_to_process.remove(random_company_id)
		# 		# prevent MySQL has gone away errors.
		# 		connection.close()
		# 		# start our worker!
		# 		worker = Worker(random_company_id)
		# 		process = multiprocessing.Process(
		# 			target=worker.start,
		# 			name=str(random_company_id)
		# 		)
		# 		process.start()
		# 		running_processes.append(process)
		# 		running_processes_cleared = False
		#
		# 	# get all active running children
		# 	active_children = multiprocessing.active_children()
		# 	active_children_ids = set()
		# 	for child in active_children:
		# 		active_children_ids.add(str(child.name))
		# 	remove_children = []
		# 	for child in running_processes:
		# 		if child.name not in active_children_ids:
		# 			remove_children.append(child)
		# 	for child in remove_children:
		# 		running_processes.remove(child)
		# 	time.sleep(3)
		# 	if len(running_processes) == 0:
		# 		running_processes_cleared = True
		# print('FINISHED CLID INTEGRATION')

	def twit_streaming(self):
		pass

	def twit_search(self):
		pass




"""
	twitter attribute
	
	created_at	: utc_String
	text		: String
	user		: user-obj
	coordinates	: coordinates-obj  OR/AND  place : place-obj
	
	entities 	: Entities obj <---HashTag are here
	"lang"		: "en"


"""
