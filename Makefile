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
	docker-compose up --build

dev-down:
	docker-compose down

# this destroys everything
dev-destroy:
	docker-compose down -v --rmi all --remove-orphans

