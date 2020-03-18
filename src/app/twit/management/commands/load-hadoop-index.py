from django.core.management.base import BaseCommand
from app.twit.utils import loadHadoopInMongo
from django.conf import settings
import os


class Command(BaseCommand):
    help = "This will seed the db with data from a json file"

    def add_arguments(self, parser):

        parser.add_argument(
            '-fp',
            '--filepath',
            type=str,
            help='where the load csv from. put csv in storage dir and use relative path'
        )

    def handle(self, *args, **kwargs):

        # retrieve args
        fp = kwargs.get('filepath', None)

        if fp:

            path = os.path.join(settings.STORAGE_DIR, fp)
            try:
                loadHadoopInMongo(path)

            except Exception as e:
                print('could not load json file error %s' % str(e))
        else:
            print('LOADING DEAFULT')
            loadHadoopInMongo()



