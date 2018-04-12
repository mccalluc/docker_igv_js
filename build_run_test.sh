#!/usr/bin/env bash
set -e

source define_repo.sh

docker pull $REPO
docker build --tag $NAME \
             --cache-from $REPO \
             context

PYTHON_SERVER_PORT=9999

# https://stackoverflow.com/a/13322667
# Finds the correct interface and ip, based on the machine's default route.
# Returns a url that will resolve to the SimpleHTTPServer we spin up below 
# so that the Docker container can make requests to files existing 
# under the cwd i.e. `./test-data/input.json`
get_python_server_url() {
    local _ip _line
    while IFS=$': \t' read -a _line ;do
        [ -z "${_line%inet}" ] &&
           _ip=${_line[${#_line[1]}>4?1:2]} &&
           [ "${_ip#127.0.0.1}" ] && echo http://$_ip:$PYTHON_SERVER_PORT && return 0
      done< <(LANG=C /sbin/ifconfig)
}

# Spin up a server so that the container can GET input data from the `test-data` dir
python -m SimpleHTTPServer $PYTHON_SERVER_PORT &
PYTHON_SERVER_PID=$!

for FIXTURE in `ls input_fixtures`; do
    docker run --env INPUT_JSON_URL=$(get_python_server_url)/input_fixtures/$FIXTURE/input.json \
    		   --detach \
               --name $FIXTURE \
               --publish 80 \
               $NAME
done

python test.py

kill $PYTHON_SERVER_PID