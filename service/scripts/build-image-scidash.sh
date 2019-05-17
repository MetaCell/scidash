#!/bin/bash

echo "Input scidash image version ('latest' by default): "

read scidashtag

if [ -z "$scidashtag" ]
then
    version="latest"
else
    version=$scidashtag
fi

tag="metacell/scidash:$version"
directory="."
dockerfile="./service/docker/Dockerfile-scidash"

docker build -t $tag -f $dockerfile $directory
