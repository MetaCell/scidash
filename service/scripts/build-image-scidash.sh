#!/bin/bash

echo "Input scidash image version ('latest' by default): "

read scidashtag

if [ -z "$scidashtag" ]
then
    version="latest"
else
    version=$1
fi

tag="metacell/scidash:$version"
directory="."
dockerfile="./service/docker/Dockerfile-scidash"

docker build --no-cache -t $tag -f $dockerfile $directory
