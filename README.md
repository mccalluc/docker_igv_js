# docker_igv_js

A Docker container to wrap IGV.js

## Development

```bash
docker build --tag igv-js context
docker run --detach --name igv-js-container --publish 8888:80 --volume data:/usr/share/nginx/html/data igv-js
# Make sure data/options.js is in place,
# and then visit http://localhost:8888/
```
