#!/bin/bash
set -e

# Wait for Postgres to be fully ready — Render Postgres can take a few seconds
# after the service reports healthy before it accepts SSL connections.
for i in 1 2 3 4 5 6 7 8 9 10; do
  echo "Attempting database migration ($i/10)..."
  if python manage.py migrate; then
    break
  fi
  if [ "$i" -eq 10 ]; then
    echo "Database migration failed after 10 attempts. Check DATABASE_URL and Postgres status."
    exit 1
  fi
  echo "Database not ready yet; retrying in 8 seconds..."
  sleep 8
done

python manage.py collectstatic --no-input

exec gunicorn cornhouse.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4
