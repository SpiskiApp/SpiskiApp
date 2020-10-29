FROM python:3.8.6

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
#COPY ./requirements.txt requirements.txt
# installation requires gcc
# https://number1.co.za/alpine-python-docker-base-image-problem-with-gcc/
# https://github.com/geerlingguy/JJG-Ansible-Windows/issues/28#issuecomment-353977003
#RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev libxml2-dev libxslt-dev \
#    && pip install --no-cache-dir -r requirements.txt \
#    && apk del .build-deps

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY finder/ .
