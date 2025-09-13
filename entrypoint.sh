#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
python manage.py migrate

# Collect static files (optional, needed for production)
# python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn delivery_app_backend.wsgi:application --bind 0.0.0.0:8000
