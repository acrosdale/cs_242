#!/bin/sh
echo "TA docker crawler script starting.....";

cd /home/django/sites/twitter/src/app

# build index from db
# 1 mb
python manage.py run-tweepy $1


