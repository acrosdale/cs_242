#!/bin/sh
echo "TA docker indexer script starting.....";

cd /home/django/sites/twitter/src/app

# build index from db
python manage.py index-tweets


