#!/usr/bin/env bash
set -e

source define_repo.sh

docker pull $REPO
docker build --tag $NAME \
             --cache-from $REPO \
             context

DATA_DIR=/tmp/docker_igv_js_`date +"%Y-%m-%d_%H-%M-%S"`
cp -a input_fixtures $DATA_DIR
# The on_startup script writes to the shared volume,
# so we copy first to avoid contamination of the fixture.

export GOOD_NAME=good_$NAME
export MISSING_ASSEMBLY_NAME=missing_assembly_$NAME

docker run --detach \
           --name $GOOD_NAME \
           --publish 80 \
           --volume $DATA_DIR/good:/var/www/data \
           $NAME

docker run --detach \
           --name $MISSING_ASSEMBLY_NAME \
           --publish 80 \
           --volume $DATA_DIR/missing_assembly:/var/www/data \
           $NAME

python test.py