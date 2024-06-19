FROM ubuntu:latest
RUN apt upgrade
RUN apt update
RUN apt install apache2 apache2-utils python3 python3-pip libapache3-mod-wsgi-py3
RUN pip3 install -r requirements.txt --no-cache-dir

COPY django-app.conf /etc/apache2/sites-available/
COPY . /var/www/html/django-app

RUN cd /var/www/html/django-app
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN cd djangoapplicationplacholder
RUN python3 manage.py collectstatic

RUN chgrp -R www-data /var/www/html
RUN a2ensite django-app
RUN /etc/init.d/apache2 restart


