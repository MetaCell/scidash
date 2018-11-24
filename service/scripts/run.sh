#!/bin/bash

python manage.py migrate
cat create_superuser.py | ./manage.py shell
python manage.py runserver 0.0.0.0:8000
