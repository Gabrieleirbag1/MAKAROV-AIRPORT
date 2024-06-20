FROM ubuntu:latest
RUN apt upgrade
RUN apt update
RUN apt install -y apache2 apache2-utils python3 python3-pip libapache2-mod-wsgi-py3 python3-venv

COPY django-app.conf /etc/apache2/sites-available/
COPY . /var/www/html/django-app

#setup venv#
RUN python3 -m venv djangovenv
RUN source djangovenv/bin/activate && pip install -r /var/www/html/django-app/requirements.txt
############


RUN python3 /var/www/html/django-app/manage.py makemigrations
RUN python3 /var/www/html/django-app/manage.py migrate
#RUN cd djangoapplicationplacholder
#RUN python3 manage.py collectstatic

RUN sudo chgrp -R www-data /var/www/html
RUN sudo a2ensite django-app
RUN sudo /etc/init.d/apache2 restart


