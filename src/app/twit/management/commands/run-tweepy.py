import tweepy
import math
import multiprocessing
from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand
from app.twit.utils import TwitStreamer


class Command(BaseCommand):
	help = "This will run tweepy and collect tweets via twitter API"
	run_default = True # this one run .sample()
	total_default = 1024*1024*1024*0.001 # 1 MB

	def add_arguments(self, parser):
		parser.add_argument('total', type=int, help='Indicates how many Gigs of data to retrieve')

		# Optional argument
		parser.add_argument('-p', '--process', type=int, help='How many processes to launch', )

	def handle(self, *args, **kwargs):

		# retrieve args
		total_data = kwargs['total']
		num_processes = kwargs['process']

		# assert vals
		assert total_data >= 1, 'total must >= 1'

		total_data *= self.total_default
		print(total_data)

		if num_processes:
			assert num_processes >= 1, 'num_process must >= 1'
			assert num_processes == len(settings.TWITTER_CREDS)
		else:
			num_processes = 1

		if num_processes == 1:
			streamer = TwitStreamer(total_data, settings.TWITTER_CREDS[0])
			streamer.start()
		else:
			# since the listen count the data in db
			# all listner will exit when all listen add x gigs to db
			total_data_split = total_data
			init_sample = False
			running_processes = []

			mylist = settings.TWEET_TRACKS
			parts = 1
			track_split = [mylist[(i * len(mylist)) // parts:((i + 1) * len(mylist)) // parts] for i in range(parts)]

			for cred in settings.TWITTER_CREDS:
				if not init_sample:
					worker = TwitStreamer(total_data_split, cred)
					process = multiprocessing.Process(target=worker.start)
					process.start()
					running_processes.append(process)
					init_sample = True
				else:
					worker = TwitStreamer(total_data_split, cred)
					process = multiprocessing.Process(target=worker.start_track, args=(track_split.pop(),))
					process.start()
					running_processes.append(process)

			for proc in running_processes:
				proc.join()






























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



