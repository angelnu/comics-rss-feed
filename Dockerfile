FROM python:3.12.4-alpine@sha256:7f15e22f496c65cffbbac5e30e7e98d60f3e3b9cc5ee5d51cf3c55ed604787c8

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
