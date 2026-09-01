#!/bin/bash
set -e

python manage.py migrate
python manage.py collectstatic --no-input

exec gunicorn cornhouse.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4
