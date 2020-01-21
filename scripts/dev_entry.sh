#!/bin/sh
echo "Dev startup script starting.....";
cd src/app
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "****Django is ready.****";
# run the command to start uWSGI

uwsgi --ini project/uwsgi.ini

#python manage.py runserver 0.0.0.0:8000
