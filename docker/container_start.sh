#!/bin/sh
export DOCKER_CONTAINER=1
cd /var/projects/mysite && python manage.py migrate --noinput && python manage.py collectstatic --noinput
supervisord -n -c /etc/supervisor/supervisord.conf