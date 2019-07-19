#!/bin/bash
echo "We are going to build the Geppetto\'s Virgo, be carefull since this"
echo "can overwrite the existing image if another one is already built" 
while true; do
    read -p "Do you wish to install to continue? [y/n] > " yn
    case $yn in
        [Yy]* ) read -p "Please type the tag you want to use for this build (default will use the latest and overwrite this). [default/user_input] > " tag;
		if [[ -z "$tag" ]]; then
		   docker build --no-cache -f Dockerfile-virgo -t metacell/scidash_virgo:latest .
		else
		   docker build --no-cache -f Dockerfile-virgo -t metacell/scidash_virgo:$tag .
		fi
                break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
