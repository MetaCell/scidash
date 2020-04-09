#!/bin/bash
sleep 120;

source ./venv/bin/activate;
cat ./service/scripts/create_superuser.py | ./manage.py shell;
make run-staging
