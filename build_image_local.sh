#!/bin/bash
mvn clean package -Dmaven.test.skip=true
docker login registry.xxxxxx.com --username=xxx --password=xxx
VERTAG="latest"
if [ -n "$1" ]
then
verTag=$1
else
verTag=$VERTAG
fi
echo "docker build and push ${verTag}"
docker build ./ -t registry.xxxxxx.com/tdc/soarui:$verTag
docker push registry.xxxxxx.com/tdc/soarui:$verTag
