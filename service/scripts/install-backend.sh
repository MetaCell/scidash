#!/bin/bash

virtualenv=false;
pygeppetto_folder="pygeppetto-django"
pygeppetto_django_repo="https://github.com/MetaCell/pygeppetto-django.git -b feature_magic $pygeppetto_folder";

while getopts "v" opt
do
    case $opt in
        v) virtualenv=true;;
    esac
done

if [ "$virtualenv" = true ] ; then
    virtualenv -p python3 ./venv;
    source ./venv/bin/activate;
fi

pip install -r requirements.txt;

git clone $pygeppetto_django_repo;

cd $pygeppetto_folder;

pip install -e .
