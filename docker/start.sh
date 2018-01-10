#!/usr/bin/env bash

set -e

virtualenv -q -p /usr/bin/python3.5 /srv/env

source /srv/env/bin/activate
pip3 install -r requirements.txt
python nltk_download.py

gunicorn --bind 0.0.0.0:5000 run:app