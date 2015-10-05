#!/usr/bin/env bash
OS_REQUIREMENTS_FILENAME="requirements.apt"

grep -v "#" ${OS_REQUIREMENTS_FILENAME} | grep -v "^$" | xargs apt-get --no-upgrade install -y;
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80