#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
poetry add whisper

python tasks.py 
python manage.py collectstatic --no-input
