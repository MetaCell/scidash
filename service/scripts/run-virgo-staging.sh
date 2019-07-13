#!/bin/bash
source ./venv-py2/bin/activate

which python
python --version

./virgo-tomcat-server/bin/startup.sh
