#!/bin/bash

node -v

root_path=$PWD;

geppetto_repo="https://github.com/openworm/org.geppetto.frontend.git"
geppetto_branch="geppetto-scidash"
extension_repo="https://github.com/MetaCell/geppetto-scidash.git"
extension_branch="geppetto-scidash"
geppetto_client_repo="https://github.com/openworm/geppetto-client.git"
geppetto_client_branch="geppetto-scidash"

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
geppetto_app_path="$geppetto_path/src/main/geppetto-scidash";

# The lines below can be commented out when we will be in line with the latest geppetto, differently
# if we try to test development this won't work since we are diverging from geppetto frontend at the moment
git ls-remote --heads --tags $geppetto_repo | grep -E 'refs/(heads|tags)/'$geppetto_branch > /dev/null

if [ $? -eq 0 ]; then
  git clone -b $geppetto_branch $geppetto_repo $geppetto_path;
else
  git clone -b development $geppetto_repo $geppetto_path;
fi

git ls-remote --heads --tags $extension_repo | grep -E 'refs/(heads|tags)/'$extension_branch > /dev/null

if [ $? -eq 0 ]; then
  git clone -b $extension_branch $extension_repo $geppetto_app_path;
else
  git clone -b development $extension_repo $geppetto_app_path;
fi

cd $geppetto_path/src/main;
rm -rf webapp;
mv geppetto-scidash webapp;
cd webapp;

git ls-remote --heads --tags $geppetto_client_repo | grep -E 'refs/(heads|tags)/'$geppetto_client_branch > /dev/null

if [ $? -eq 0 ]; then
  git clone -b $geppetto_client_branch $geppetto_client_repo;
else
  git clone -b development $geppetto_client_repo;
fi

npm install

