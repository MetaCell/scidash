#!/bin/bash

tag="metacell/scidash"
directory="."
dockerfile="Dockerfile"

docker build -t $tag -f $dockerfile $directory
