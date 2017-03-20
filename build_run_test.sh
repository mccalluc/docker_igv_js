#!/usr/bin/env bash
set -e

NAME=docker_igv_js
docker build --tag $NAME context
docker run --detach \
           --publish 80 \
           --volume `pwd`/data_fixture:/var/www/data \
           $NAME
python test.py