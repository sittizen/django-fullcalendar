#!/bin/bash
source ../.env
set -e
LOGFILE=/home/django/django-fullcalendar/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=django
GROUP=django
ADDRESS=127.0.0.1:8001
cd /home/django/django-fullcalendar/website
export DJANGO_ENVIRONMENT=$PRJ_ENV
source /home/django/.virtualenvs/django-fullcalendar/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE --settings website.settings