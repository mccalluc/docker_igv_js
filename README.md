# docker_igv_js [![Build Status](https://travis-ci.org/refinery-platform/docker_igv_js.svg?branch=master)](https://travis-ci.org/refinery-platform/docker_igv_js)

A Docker container to wrap IGV.js

## Motivation

Visualizations in [Refinery](https://github.com/refinery-platform/) are provided by Docker containers.
The link between Refinery and the Docker containers is [django_docker_engine](https://github.com/refinery-platform/django_docker_engine).
A container may provide back-end services to a visualization, or after start up it may just serve static html and js,
as is the case here. In either case the input files are provided in a directory which is mounted on a predetermined path.

## Add new genomes

The IGV instance will look for genome reference files in a particular S3 bucket. To add reference files for a new assembly,
check out [get-reference-genomes](https://github.com/refinery-platform/get-reference-genomes) and run `genome-to-s3.sh`.

## Development

Clone the repository, make sure Docker is installed, and then:

```
pip install -r requirements.txt
python test.py
```

After the tests run the container is left up, with the local url where it can be accessed.

## Release

Successful Github tags and PRs will prompt Travis to push the built image to Dockerhub. For a new version number:

```
git tag v0.0.x && git push origin --tags
```
