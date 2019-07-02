#!/bin/bash
echo "We are going to build the scidash image, be carefull since this"
echo "can overwrite the existing image if another one is already running" 
while true; do
    read -p "Do you wish to install to continue?" yn
    case $yn in
        [Yy]* ) read -p "Please type the tag you want to use for this build (default will use the latest and overwrite this)" tag;
		if [[ -z "$tag" ]]; then
		   docker build -f Dockerfile-scidash -t metacell/scidash:latest
		else
		   docker build -f Dockerfile-scidash -t metacell/scidash:$tag
		fi
                break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
