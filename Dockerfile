FROM python:3.11-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN apk update \
&& apk add --no-cache git \
&& pip install --upgrade pip \
&& pip install -r requirements.txt --no-cache-dir

COPY . .