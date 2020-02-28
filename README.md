# CS242 Project

## Project Structure

## How to get db
`from twit.utils import GetMongo_client`.     
`cs_242/src/app/twit/utils.py` , the class of GetMongo_client, get the mogodb variable

## Usage


### Capture the stream
1. After compose,enter the `django_twitter` container
```bash
sudo docker exec -it django_twitter bash
```

if not work tired:
`docker-compose build --no-cache`

2. Run management cmds
```bash
cd src/app

python manage.py run-tweepy 1 # this collect 1Mb of data

python manage.py run-tweepy 1 -p 2 # this collect 1Gb of data with 2 parallel process limit 1 per account

python manage.py load-csv -fp 'twit_tweet-standard.json' # loads the json file name.json located in resources/storage into db

python manage.py index-tweets # creates two indexes ['tweet_index', 'tag_index']

```
3. Download the data from MongoDB Express
	* Go to [https://localhost:8081](https://localhost:8081), click on **django**
	* Export data from `twit_tweet`

## Changelog
* first commit
	* skeleton code for cs 242 project. made with django, mongodb, docker
* Jan 31
	* Complete Twitter crawling

