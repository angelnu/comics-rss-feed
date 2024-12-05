FROM python:3.13.1-alpine@sha256:804ad02b9ba67ea1f8307eeb6407b121c6bd6bb19d3f182aae166821eb59d6a4

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
