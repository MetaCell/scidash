#!/bin/bash

pushd /home/metacell/deployment/scidash/service/deployment
/usr/local/bin/docker-compose up -d
popd
