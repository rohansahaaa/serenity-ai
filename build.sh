#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate