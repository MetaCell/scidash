#!/bin/bash

echo "Input scidash image version ('latest' by default): ";

read scidashtag;

if [ -z "$scidashtag" ]
then
    docker push metacell/scidash;
else
    docker push metacell/scidash:$scidashtag;
fi

