FROM python:3.13.6-alpine@sha256:af1fd7a973d8adc761ee6b9d362b99329b39eb096ea3c53b8838f99bd187011e

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
