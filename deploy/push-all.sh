#!/bin/bash

echo "Input db image version ('latest' by default): "

read dbtag

echo "Input scidash image version ('latest' by default): "

read scidashtag

if [ -z "$1" ]
then
    docker push metacell/scidash-db
    docker push metacell/scidash
else
    docker push metacell/scidash-db:$dbtag
    docker push metacell/scidash:$scidashtag
fi

