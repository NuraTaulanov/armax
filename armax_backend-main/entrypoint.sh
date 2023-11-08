#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic
gunicorn --workers=8 --error-logfile '-' --access-logfile '-' --access-logformat '%(t)s "%(r)s" %(s)s %(b)s' config.wsgi:application --bind 0.0.0.0:8000

exec "$@"