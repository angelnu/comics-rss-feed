FROM python:3.11.0-alpine@sha256:ef8ab2f0859e5c68ae08df5ce9748c030b1c5989d728e34a0ef36a5a746a676c

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
