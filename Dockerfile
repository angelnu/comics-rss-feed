FROM python:3.10.8-alpine@sha256:85a0c5586db9c0b4777f202dbecba059ff82f129ba09c7b27df1d88797b7ad93

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
