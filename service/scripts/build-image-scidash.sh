#!/bin/bash

if [ -z "$1" ]
then
    version="latest"
else
    version=$1
fi

tag="metacell/scidash:$version"
directory="."
dockerfile="./deploy/docker/Dockerfile-scidash"

docker build --no-cache -t $tag -f $dockerfile $directory
