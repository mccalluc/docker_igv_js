FROM nginx:1.10.3-alpine

RUN mkdir -p /usr/share/nginx/html
WORKDIR /usr/share/nginx/html

RUN wget http://igv.org/web/release/1.0.7/igv-1.0.7.js
RUN wget http://igv.org/web/release/1.0.7/igv-1.0.7.css

RUN wget http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js
RUN wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css
RUN wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js

COPY index.html .

VOLUME data