#!/bin/bash

echo "Input db image version ('latest' by default): "

read dbtag

echo "Input scidash image version ('latest' by default): "

read scidashtag

./deploy/scripts/build-image-db.sh $dbtag
./deploy/scripts/build-image-scidash.sh $scidashtag
