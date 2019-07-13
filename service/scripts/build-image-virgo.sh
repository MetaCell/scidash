#!/bin/bash

echo "Input virgo image version ('latest' by default): "

read virgotag

if [ -z "$virgotag" ]
then
    version="latest"
else
    version=$virgotag
fi

tag="metacell/geppetto-virgo:$version"
directory="."
dockerfile="./service/docker/Dockerfile-virgo"

docker build -t $tag -f $dockerfile $directory

