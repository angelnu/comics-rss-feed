FROM python:3.11.0-alpine@sha256:4479c584c3a69c4ac1d997e12716794506a848976ad3693190a1af14c8ed759a

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
