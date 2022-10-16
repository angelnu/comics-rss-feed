FROM python:3.10.8-alpine@sha256:3bfac1caa31cc6c0e796b65ba936f320d1e549d80f5ac02c2e4f83a0f04af3aa

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
