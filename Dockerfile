FROM python:3.14-slim

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
RUN playwright install && \
    playwright install-deps && \
    playwright install chromium
COPY *.py /usr/local/bin/

RUN mkdir /data
VOLUME /data
WORKDIR /data

CMD [ "getcomics_RSS.py" ]

ARG IMAGE_SOURCE
#https://github.com/k8s-at-home/template-container-image
LABEL org.opencontainers.image.source=$IMAGE_SOURCE 
