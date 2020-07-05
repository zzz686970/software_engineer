#!/bin/bash

## pull latest container
docker pull jenkins

## setup local configurration folder
## should always be in a jenkins folder when running this script

export CONFIG_FOLDER=$PWD/config
mkdir $CONFIG_FOLDER
chown 1000 $CONFIG_FOLDER

## start container
docker run --restart=always -d -p 49001:8080 -v $CONFIG_FOLDER:/var/jenkins_home:z \
# -e http_proxy='http://proxy.com:8080' \
# -e http_proxy='https://proxy.com:8080' \
--name jenkins -t jenkins

docker logs --follow jenkins