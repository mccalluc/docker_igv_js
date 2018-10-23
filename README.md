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

After the tests run successfully the containers used for testing are killed.

## Running and accessing the container

- The docker_igv_js container can be run by pointing to valid `input.json` file by url: 
    - `docker run -p 8080:80 -e INPUT_JSON_URL=https://raw.githubusercontent.com/refinery-platform/docker_igv_js/master/input_fixtures/good/input.json gehlenborglab/docker_igv_js`

- Or an `input.json` file can be constructed and passed to the container directly through the envvar: `INPUT_JSON`.
  - ```
    docker run -p 8080:80 -e INPUT_JSON='
      {
        "node_info": {
          "<some unique key>": {
            "file_url": "<url to an IGV-compatible file>",
            "node_solr_info": {
              "name": "<some descriptor of your file to be a prefix in your track name>"
            }
          }
        },
        "parameters": [
          {
            "name": "Genome Build",
            "value": "hg19"
          }
        ]
      }' gehlenborglab/docker_igv_js
    ```

- Visit http://localhost:8080


> **Note:** The current intentions of this project are to satisfy the needs of the [refinery-platform](https://github.com/refinery-platform/refinery-platform), which currently has a strict way of passing input data to the underlying application (as seen above). Decoupling this tool, and providing a more general purpose solution has been [talked of here](https://github.com/refinery-platform/docker_igv_js/issues/29#issuecomment-431904804).

## Release

Successful Github tags and PRs will prompt Travis to push the built image to Dockerhub. For a new version number:

```
git tag v0.0.x && git push origin --tags
```
