
# Image URL to use all building/pushing image targets
IMG ?= $(shell basename $(CURDIR)):latest

# Build the docker image
docker-build:
	docker build . -t ${IMG}

# Push the docker image
docker-push:
	docker push ${IMG}