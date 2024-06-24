# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
WORKDIR /app 
COPY django-compose-structure/makarov_structure/requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY django-compose-structure/makarov_structure/ /app
COPY django-compose-structure/makarov_structure/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
RUN python3 manage.py makemigrations
ENTRYPOINT ["sh", "-c"]
CMD ["/wait-for-it.sh"]

