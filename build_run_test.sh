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
# so we copy first to avoid contamination of the fixture in source.

for FIXTURE in `ls input_fixtures`; do
    docker run --detach \
               --name $FIXTURE \
               --publish 80 \
               --volume $DATA_DIR/$FIXTURE:/var/www/data \
               $NAME
done

python test.py