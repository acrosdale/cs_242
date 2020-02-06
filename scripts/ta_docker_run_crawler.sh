#!/bin/sh
echo "TA docker crawler script starting.....";

cd src/app

# build index from db
# 1 Gb
python manage.py run-tweepy 1


