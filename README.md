# CS242 Project

## Project Structure

## How to get db

`from twit.utils import GetMongo_client`.  
`cs_242/src/app/twit/utils.py` , the class of GetMongo_client, get the mogodb variable

## Usage

1. Within the root level of the project dir [/cs_242/] run ```docker-compose up```. This will start all the required containers.

2. Before using the search engine load data into the db, create in the lucene and hadoop index. the step to do so are below.

3. After everthing is up and running click the link to go to the apps main page [http://localhost:1337/twit/](http://localhost:1337/twit/). 

### Capture the stream

1. After compose up, enter the `django_twitter` container

```docker exec -it django_twitter bash```

2. Run management cmds

```bash
cd src/app

python manage.py run-tweepy 1 # this collect 1Mb of data
# OR
python manage.py run-tweepy 1 -p 2 # this collect 1Gb of data with 2 parallel process limit 1 per account

```

### Load data into DB
1. download the tweets.json file from google drive [tweets.json](https://drive.google.com/file/d/1R18jd-Gaq2OrClIPF6-gOkllurw3iAyL/view?usp=sharing). Only RMail account can download the link.

2. place the json file in the resources/storage/ directory of the app

3. After compose up, enter the `django_twitter` container

```docker exec -it django_twitter bash```

2. Run management cmds

```
cd src/app

python manage.py load-csv -fp 'downloaded_file_name'

# OR load sample

python manage.py load-csv -fp 'twit_tweet-standard.json'

# files MUST exists in resources/storage/ directory
# the resources/storage/ path is implied
# this file's full path would be resources/storage/twit_tweet-standard.json
```

### create index [Lucene]
1. After compose up, enter the `django_twitter` container

```docker exec -it django_twitter bash```

2. Run management cmds
```
cd src/app
python manage.py index-tweets 

# creates two indexes ['tweet_index', 'tag_index']
# indexes are located in resources/storage/index_name
```
### create index [Hadoop]
1. After compose up, enter the `namenode` container

```docker exec -it namenode bash```

2. Run management cmds

```
cd home/hadoopMR
sh exec.sh  

# sh exec.sh works as such: it exports the data from 'twit_tweet' collection in csv 
# and runs the Hadoop Map-Reduce jobs with the data, which internally calls 
# the ranking function and stores the final indexed-ranked documents in the DB.
```
### DB GUI | MongoDB Express [MongoDB GUI]
1. After compose up, Go to [http://localhost:8081/db/django/](http://localhost:8081/db/django/), 
   - `twit_tweet` collection contains all tweets data from twitter
   - `ranked_index` collection contains the hadoop inverted index

## Changelog

- first commit \* skeleton code for cs 242 project. made with django, mongodb, docker
- Jan 31 \* Complete Twitter crawling
