# CS242 Project

## Project Structure
`cs_242/src/app/twit/utils.py` , the class of GetMongo_client, get the mogodb variable

## Usage


### Capture the stream
1. After compose,enter the `django_twitter` container
```bash
sudo docker exec -it django_twitter bash
```

if not work tired:
`docker-compose build --no-cache`

2. Get into management shell
```bash
python src/app/manage.py shell
```
3. Use the following in interactive Python shell. Replace `size` with the number of bytes to collect
```python
from twit.utils import TwitStreamer
size = 1024*1024*1024*5 # Get 5GB of data
ts = TwitStreamer(size)
ts.start()
```
4. Download the data from MongoDB Express
	* Go to [https://localhost:8081](https://localhost:8081), click on **django**
	* Export data from `twit_tweet`

## Changelog
* first commit
	* skeleton code for cs 242 project. made with django, mongodb, docker
* Jan 31
	* Complete Twitter crawling

