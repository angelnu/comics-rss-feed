FROM python:3.11.0-alpine@sha256:ec7ff85cfca09fc0d9b4bae53f0d0f2ee164c844ba509e641917432d82e9dae3

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
