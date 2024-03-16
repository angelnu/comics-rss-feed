FROM python:3.12.2-alpine@sha256:6deafe0dd6043df014df7b78c4da976f008a77d160c8d1857dd83b50d88b2aae

RUN pip3 install requests==2.*

COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source $IMAGE_SOURCE 
