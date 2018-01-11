#!/usr/bin/env bash
# TODO: Do not run pip install on each docker run; use absolute paths

set -e

virtualenv -q -p /usr/bin/python3.5 ./env

source ./env/bin/activate
pip install -r ./flask/requirements.txt
python ./flask/nltk_download.py

gunicorn --chdir ./flask --bind 0.0.0.0:5000 run:app