#!/bin/sh
echo "Dev startup script starting.....";
cd src/app
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "****Django is ready.****";

# run test
py.test ../../tests -v --cov-report term --cov=. --cov-report=html --cov-config=../../.coveragerc -o cache_dir=./run/.pytest_cache