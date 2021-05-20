#!/bin/bash

docker build -f Dockerfile-virgo -t metacell/scidash_virgo:latest ../..
docker build -f Dockerfile-postgres -t metacell/scidash_db:latest ../..
docker build -f Dockerfile-scidash -t metacell/scidash:latest ../..
