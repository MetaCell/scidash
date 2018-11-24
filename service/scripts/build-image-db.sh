#!/bin/bash

if [ -z "$1" ]
then
    version="latest"
else
    version=$1
fi

tag="metacell/scidash-db:$version"
directory="."
dockerfile="./deploy/docker/Dockerfile-postgres"

docker build -t $tag -f $dockerfile $directory
