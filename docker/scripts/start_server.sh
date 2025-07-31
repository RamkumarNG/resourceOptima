#!/bin/bash

echo "🚀 Starting Django application with Gunicorn..."

# Run migrations
python manage.py migrate

# Initialize the app (if needed)
python manage.py initapp

# Start Gunicorn with 1 worker binding to port 8000
exec gunicorn app.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --log-level info
