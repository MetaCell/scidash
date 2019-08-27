#!/bin/bash

if [ -z `/usr/local/bin/docker-compose ps -q deployment_scidash_1` ] || [ -z `/usr/bin/docker ps -q --no-trunc | grep $(/usr/local/bin/docker-compose ps -q deployment_scidash_1)` ]; then
	/usr/local/bin/scidash_start.sh
else
	exit 0
fi
