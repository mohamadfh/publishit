#!/bin/sh

# Run migrations
python manage.py makemigrations && python manage.py migrate

# Collect static files only if the static directory is empty
if [ ! -d "/usr/src/app/staticfiles" ] || [ -z "$(ls -A /usr/src/app/staticfiles)" ]; then
    python manage.py collectstatic --noinput
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 3 --timeout 120
