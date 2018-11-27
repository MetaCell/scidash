#!/bin/bash

echo "Input db image version ('latest' by default): ";

read dbtag;

if [ -z "$dbtag" ]
then
    docker push metacell/scidash-db;
else
    docker push metacell/scidash-db:$dbtag;
fi
