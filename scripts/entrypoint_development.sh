#!/bin/sh

set -e

python manage.py wait_for_db &&
python manage.py migrate &&
python manage.py collectstatic --no-input &&
python manage.py createsu &&
python manage.py runserver 0.0.0.0:8000