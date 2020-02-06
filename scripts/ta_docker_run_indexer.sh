#!/bin/sh
echo "TA docker indexer script starting.....";

cd src/app

# build index from db
python manage.py index-tweets


