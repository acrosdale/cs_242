#!/bin/sh
echo "TA script starting.....";

#docker-compose  build --no-cache

docker-compose up --detach

# enter docker
docker exec -it django_twitter bash
