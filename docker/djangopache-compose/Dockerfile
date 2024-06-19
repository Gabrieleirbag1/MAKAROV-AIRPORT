FROM ubuntu:latest
RUN sudo apt upgrade
RUN sudo apt update
RUN sudo apt install apache2 apache2-utils python3 python3-pip libapache3-mod-wsgi-py3
RUN sudo pip3 install -r requirements.txt --no-cache-dir

COPY django-app.conf /etc/apache2/sites-available/
COPY . /var/www/html/django-app

RUN cd /var/www/html/django-app
RUN sudo python3 manage.py makemigrations
RUN sudo python3 manage.py migrate
#RUN cd djangoapplicationplacholder
#RUN sudo python3 manage.py collectstatic

RUN sudo chgrp -R www-data /var/www/html
RUN sudo a2ensite django-app
RUN sudo /etc/init.d/apache2 restart


