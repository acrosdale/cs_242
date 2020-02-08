#!/bin/sh
echo "TA docker seed db script starting.....";

cd /home/django/sites/twitter/src/app

# Seed database. MongoDb
# load the file twit_tweet-standard.json in resources/storage
# all file have the relative path to resources/storage
# store all file there
python manage.py load-csv -fp 'twit_tweet-standard.json'




