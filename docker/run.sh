#!/bin/bash
if [ -n "$1" ]; then
docker run -d --name scidash --publish=8080:8080 -e BRANCH=$1 metacell/scidash:latest
else
docker run -d --name scidash --publish=8080:8080 metacell/scidash:latest
fi
echo "wait 1 minute for server to come up and then point browser to http://0.0.0.0:8000"
echo "use logs.sh to see logs, login.sh to log into the running container, stop.sh to stop the server"
