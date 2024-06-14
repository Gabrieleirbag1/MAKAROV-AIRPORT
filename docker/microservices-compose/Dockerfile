# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS micropy
WORKDIR /app
COPY microservices-compose/requirements.txt /app
RUN ls -l
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app

