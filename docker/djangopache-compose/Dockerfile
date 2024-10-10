FROM debian:bookworm-slim

COPY djangopache-compose/ /var/www/html/django-app

RUN apt update \
        && apt install --no-install-recommends --no-install-suggests -y apache2 apache2-utils python3 p>
        && python3 -m venv /var/www/html/django-app/djangovenv \
        && /var/www/html/django-app/djangovenv/bin/pip install --no-cache-dir -r /var/www/html/django-a>
        && /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py makemigrat>
        && /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py migrate \
        && /var/www/html/django-app/djangovenv/bin/python /var/www/html/django-app/manage.py collectsta>
        && rm -rf /var/www/html/django-app/makarov_gp/static \
        && chmod -R 777 /var/www/html/django-app \
        && chgrp -R www-data /var/www/html

COPY djangopache-compose/django-app.conf /etc/apache2/sites-available/


RUN a2ensite django-app
RUN a2dissite 000-default.conf
