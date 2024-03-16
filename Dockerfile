FROM python:3.12.2-alpine@sha256:fa2fd94b02c2eacf55775c37fee40752275ac7710d0f7c8dc709ccc67917b332

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
