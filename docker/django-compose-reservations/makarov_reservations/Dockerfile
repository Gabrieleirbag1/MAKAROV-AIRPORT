# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
WORKDIR /app 
COPY django-compose-reservations/requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY django-compose-reservations/ /app
COPY django-compose-reservations/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
RUN python3 manage.py makemigrations
ENTRYPOINT ["sh", "-c"]
CMD ["/wait-for-it.sh"]

