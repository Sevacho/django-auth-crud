#!/usr/bin/env bash
# exit on error
#no sube nada 
set -o errexit
#poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input 
python manage.py migrate