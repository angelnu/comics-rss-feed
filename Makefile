#!make
-include envfile
export $(shell sed 's/=.*//' envfile)

# Image URL to use all building/pushing image targets
IMG ?= $(shell basename $(CURDIR)):latest

test: docker-build
	docker run \
	-e RSS_URL=${RSS_URL} \
    -e RSS_LOGIN=${RSS_LOGIN} \
    -e RSS_PASSWORD=${RSS_PASSWORD} \
    -e XML_FOLDER=${XML_FOLDER} \
    -e RSS_SCRAPPER_URL=${RSS_SCRAPPER_URL} \
	${IMG}

# Build the docker image
docker-build:
	docker build . -t ${IMG}

# Push the docker image
docker-push:
	docker push ${IMG}