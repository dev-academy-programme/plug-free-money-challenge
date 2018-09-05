FROM python:3.6.5-alpine3.6 
LABEL author Harrison Symes <symeshjb@gmail.com>

ARG password

RUN apk update && \
    apk add --update --virtual build_deps alpine-sdk libffi-dev python3-dev openssl-dev linux-headers && \
    apk add libzmq

RUN pip install plug==0.0.14 -i http://plug:$password@pypi.qad.re/simple --trusted-host=pypi.qad.re

RUN pip install plug_top==0.0.2 -i http://plug:$password@pypi.qad.re/simple --trusted-host=pypi.qad.re

COPY . /app

RUN pip install /app && \
    apk del build_deps && \
    rm -rf /app
