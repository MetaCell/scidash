#!/bin/bash

geppetto_path="./static/org.geppetto.frontend";

if [ -d "$geppetto_path" ]; then
    rm -rf $geppetto_path;
fi

./service/scripts/install-frontend.sh
