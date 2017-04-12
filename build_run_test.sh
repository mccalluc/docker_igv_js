#!/usr/bin/env bash
set -e

# On travis, the script is sourced, so these will be available outside:
OWNER=gehlenborglab
NAME=docker_igv_js
REPO=$OWNER/$NAME

# For local development, sudo is not needed.
[ -z "$TRAVIS" ] && DOCKER='docker' || DOCKER='sudo docker'

$DOCKER pull $REPO
$DOCKER build --tag $NAME \
             --cache-from $REPO \
             context

DATA_DIR=/tmp/docker_igv_js_`date +"%Y-%m-%d_%H-%M-%S"`
cp -a data_fixture $DATA_DIR
# The on_startup script writes to the shared volume,
# so we copy first to avoid contamination of the fixture.

$DOCKER run --detach \
           --name $NAME \
           --publish 80 \
           --volume $DATA_DIR:/var/www/data \
           $NAME

python test.py $NAME