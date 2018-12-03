#!/bin/bash

echo "Input db image version ('latest' by default): "

read dbtag

if [ -z "$dbtag" ]
then
    version="latest"
else
    version=$1
fi

tag="metacell/scidash-db:$version"
directory="."
dockerfile="./service/docker/Dockerfile-postgres"

docker build -t $tag -f $dockerfile $directory
