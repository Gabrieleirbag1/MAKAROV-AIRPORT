FROM ubuntu:latest

RUN apt upgrade

RUN apt install apache2 apache2-utils python3 python3-pip libapache3-mod-wsgi-py3
RUN pip3 install -r requirements.txt --no-cache-dir

COPY django-app.conf /etc/apache2/sites-available/
COPY . /var/www/html

RUN


