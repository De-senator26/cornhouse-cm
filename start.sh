#!/bin/bash
set -e

for i in 1 2 3 4 5 6; do
  echo "Attempting database migration ($i/6)..."
  if python manage.py migrate; then
    break
  fi
  if [ "$i" -eq 6 ]; then
    echo "Database migration failed after repeated attempts. Check DATABASE_URL and Postgres status."
    exit 1
  fi
  echo "Database not ready yet; retrying in 5 seconds..."
  sleep 5
done

python manage.py collectstatic --no-input

exec gunicorn cornhouse.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4
