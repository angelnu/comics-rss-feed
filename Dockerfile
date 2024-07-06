FROM python:3.12.4-alpine@sha256:b7662fc33e07f05fb2f579c3634e1e4d2e30c02553397c6c24f775cb360dbc03

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
