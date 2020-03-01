#!/bin/bash

branchname=$1
if [ -z "$branchname" ]
then
  branchname="development"
fi

echo "We are going to build the scidash Database, be carefull since"
echo " this can overwrite the existing container if another one is already running" 
while true; do
    read -p "Do you wish to install to continue? [y/n] > " yn
    case $yn in
        [Yy]* ) read -p "Please type the tag you want to use for this build (default will use the latest and overwrite this). [latest/user_input] > " tag;
		if [[ -z "$tag" ]]; then
		   docker build --build-arg SCIDASH_BRANCH=${branchname} -f Dockerfile-postgres -t metacell/scidash_db:latest .
		else
		   docker build --build-arg SCIDASH_BRANCH=${branchname} -f Dockerfile-postgres -t metacell/scidash_db:$tag .
		fi
                break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
