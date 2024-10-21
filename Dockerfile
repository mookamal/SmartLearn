FROM python:3.12-slim-bullseye

ENV : show logs
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install gcc libc-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app/