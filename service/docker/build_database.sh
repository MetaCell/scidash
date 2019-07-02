#!/bin/bash
echo "We are going to build the scidash Database, be carefull since"
echo " this can overwrite the existing container if another one is already running" 
while true; do
    read -p "Do you wish to install to continue?" yn
    case $yn in
        [Yy]* ) read -p "Please type the tag you want to use for this build (default will use the latest and overwrite this)" tag;
		if [[ -z "$tag" ]]; then
		   docker build -f Dockerfile-postgres -t metacell/scidash_db:latest
		else
		   docker build -f Dockerfile-postgres -t metacell/scidash_db:$tag
		fi
                break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
