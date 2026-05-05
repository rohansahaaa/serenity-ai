#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --no-input