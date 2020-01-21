SHELL := /usr/bin/env bash

####################
## Compose DEV Commands ##
####################

# this build the dev env
dev-setup: dev-build dev-up

# create image/services based on the dev compose file
dev-build:
	docker-compose build

dev-up:
	docker-compose up

dev-destroy:
	docker-compose down

##########################
## Compose Test Commands #
##########################

#run test
test-run-web:
	docker-compose run web SCRIPT=dev_test.sh

# start test build and run test suite
test: test-run-web

