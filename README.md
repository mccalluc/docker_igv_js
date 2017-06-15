# docker_igv_js [![Build Status](https://travis-ci.org/refinery-platform/docker_igv_js.svg?branch=master)](https://travis-ci.org/refinery-platform/docker_igv_js)

A Docker container to wrap IGV.js

## Motivation

Visualizations in [Refinery](https://github.com/refinery-platform/) are provided by Docker containers.
The link between Refinery and the Docker containers is [django_docker_engine](https://github.com/refinery-platform/django_docker_engine).
A container may provide back-end services to a visualization, or after start up it may just serve static html and js,
as is the case here. In either case the input files are provided in a directory which is mounted on a predetermined path.

## Development

Clone the repository, make sure Docker is installed, and then:

```
pip install -r requirements.txt
./build_run_test.sh
```

After the tests run the container is left up, and the port it's running on will printed.

## Release

Successful Github tags and PRs will prompt Travis to push the built image to Dockerhub. For a new version number:

```
git tag v0.0.x && git push origin --tags
```
