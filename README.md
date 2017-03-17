# docker_igv_js

A Docker container to wrap IGV.js

## Development

```bash
docker build --tag mccalluc/igv-js context
docker run --detach \
           --name igv-js-container \
           --publish 8888:80 \
           --volume `pwd`/data:/usr/share/nginx/html/data \
           mccalluc/igv-js
cp options-demo.js data/options.js
```

Visit [http://localhost:8888/]
