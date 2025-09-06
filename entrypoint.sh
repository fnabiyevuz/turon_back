#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL to be ready..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started successfully."
fi

# Django migration va static fayllarni yig'ib olamiz
python manage.py migrate
python manage.py collectstatic --noinput

# Gunicorn yoki boshqa serverni ishga tushirish (masalan)
exec "$@"
