#!/bin/bash

node -v

root_path=$PWD;

geppetto_repo="https://github.com/openworm/org.geppetto.frontend.git"
geppetto_branch="v0.4.2-beta"
extension_repo="https://github.com/MetaCell/geppetto-scidash.git"
extension_branch="4.0.2"

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -b|--branch)
    geppetto_branch="$2"
    extension_branch="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

geppetto_path="./static/org.geppetto.frontend";
geppetto_app_path="$geppetto_path/src/main/webapp";
extension_path="$geppetto_app_path/extensions/geppetto-scidash";
sample_config_path="./service/geppetto/GeppettoConfiguration.json";
actual_config_path="$geppetto_app_path/GeppettoConfiguration.json";

# The lines below can be commented out when we will be in line with the latest geppetto, differently
# if we try to test development this won't work since we are diverging from geppetto frontend at the moment
#git ls-remote --heads --tags $geppetto_repo | grep -E 'refs/(heads|tags)/'$geppetto_branch > /dev/null

#if [ $? -eq 0 ]; then
#  git clone -b $geppetto_branch $geppetto_repo $geppetto_path;
#else
  git clone -b v0.4.2-beta $geppetto_repo $geppetto_path;
#fi

git ls-remote --heads --tags $extension_repo | grep -E 'refs/(heads|tags)/'$extension_branch > /dev/null

if [ $? -eq 0 ]; then
  git clone -b $extension_branch $extension_repo $extension_path;
else
  git clone -b 4.0.2 $extension_repo $extension_path;
fi

cd $geppetto_app_path;

npm install

cd $root_path;

cp $sample_config_path $actual_config_path;
