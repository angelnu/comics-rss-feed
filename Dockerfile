FROM python:3.11.0-alpine@sha256:2a068b9442f61f4480306d44e3b166bfe3343761e9bd57c38f66302ebf28fd9e

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
