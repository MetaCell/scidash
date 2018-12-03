#!/bin/bash

source ./venv/bin/activate;
python manage.py migrate;
cat ./service/scripts/create_superuser.py | ./manage.py shell;
python manage.py runserver 0.0.0.0:8000;
