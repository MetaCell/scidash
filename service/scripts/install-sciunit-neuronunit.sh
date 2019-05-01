#!/bin/bash

root_path=$PWD;

sciunit_repo="https://github.com/scidash/sciunit.git -b dev"
neuronunit_repo="https://github.com/scidash/neuronunit.git -b dev"
venv="./venv/bin/activate"

sciunit_path="$root_path/sciunit"
neuronunit_path="$root_path/neuronunit"
proper_requirements_path="$root_path/service/sciunit/requirements.txt"
sciunit_requirements_path="$sciunit_path/requirements.txt"

git clone $sciunit_repo $sciunit_path
git clone $neuronunit_repo $neuronunit_path

cp $proper_requirements_path $sciunit_requirements_path

source $venv

cd $sciunit_path

pip install -e .

cd $root_path

cd $neuronunit_path

pip install -e .

cd $root_path
