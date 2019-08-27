#!/bin/bash

if /usr/bin/docker exec `docker ps | grep 'deployment_scidash_1' | awk '{ print $1 }'` bash -c 'ps aux | grep "scidash.main beat"' | grep celery; then 
	exit 0
else
	/usr/bin/docker exec -d `docker ps | grep 'deployment_scidash_1' | awk '{ print $1 }'` bash -c 'rm /app/scidash/celerybeat.pid; source /app/scidash/venv/bin/activate; make run-celery-beat'
fi
