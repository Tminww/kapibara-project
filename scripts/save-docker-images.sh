#!/bin/bash

APP_PATH=$(pwd)/../

cd $APP_PATH
docker save -o kapibara-images.tar $(docker-compose --file docker-compose.inner.yml config --images)
