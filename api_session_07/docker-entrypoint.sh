#!/bin/sh
set -e

flask --app app db upgrade

exec gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app