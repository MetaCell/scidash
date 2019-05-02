#!/bin/bash

echo "Input scidash image version ('latest' by default): "

read scidashtag

echo "Input virgo location ('$SERVER_HOME' by default): "

read virgo_home

if [ -z "$scidashtag" ]
then
    version="latest"
else
    version=$scidashtag
fi

cp $virgo_home ./

tag="metacell/scidash:$version"
directory="."
dockerfile="./service/docker/Dockerfile-scidash"

docker build --no-cache -t $tag -f $dockerfile $directory
