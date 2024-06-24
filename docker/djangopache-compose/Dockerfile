FROM ubuntu:latest
RUN apt upgrade
RUN apt update
RUN apt install -y apache2 apache2-utils python3 python3-pip libapache2-mod-wsgi-py3 python3-venv

COPY djangopache-compose/django-app.conf /etc/apache2/sites-available/
COPY djangopache-compose/ /var/www/html/django-app

# Set up virtual environment and install Python dependencies
RUN python3 -m venv /var/www/html/django-app/djangovenv && \
    /var/www/html/django-app/djangovenv/bin/pip install -r /var/www/html/django-app/requirements.txt

RUN /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py makemigrations && \
    /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py migrate

RUN /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py collectstatic --noinput --clear

RUN chgrp -R www-data /var/www/html
RUN a2ensite django-app
RUN a2dissite 000-default.conf
CMD ["service", "apache2", "start"]


