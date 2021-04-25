#!/bin/bash

virtualenv=false;
pygeppetto_folder="pygeppetto-django"
pygeppetto_branch="geppetto-scidash"
pygeppetto_django_repo="https://github.com/MetaCell/pygeppetto-django.git"

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -v|--virtualenv)
    virtualenv=true
    shift # past argument
    ;;
    -b|--branch)
    pygeppetto_branch="$2"
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

if [ "$virtualenv" = true ] ; then
    virtualenv -p python3.6 ./venv;
    source ./venv/bin/activate;
fi

python -m pip install pip==9.0.3
pip install -r requirements.txt;
# pip uninstall -y sciunit
# pip install git+git://github.com/ddelpiano/sciunit@4.0.0#egg=sciunit

pip install git+git@github.com:MetaCell/scidash-api.git@master#egg=scidash_api

git ls-remote --heads --tags $pygeppetto_django_repo | grep -E 'refs/(heads|tags)/'$pygeppetto_branch > /dev/null

if [ $? -eq 0 ]; then
  git clone -b $pygeppetto_branch $pygeppetto_django_repo $pygeppetto_folder
else
  git clone -b geppetto-scidash $pygeppetto_django_repo $pygeppetto_folder
fi

cd $pygeppetto_folder;

pip install -e .
