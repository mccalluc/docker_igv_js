FROM ubuntu:16.04

# TODO: Combine to a single line
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y wget
# TODO    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www
# TODO
#RUN groupadd -r www && useradd -r -g www www
#RUN chown www:www .
#USER www

RUN wget http://igv.org/web/release/1.0.7/igv-1.0.7.js
RUN wget http://igv.org/web/release/1.0.7/igv-1.0.7.css

RUN wget http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js
RUN wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css
RUN wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js

COPY . .
# TODO: Files which will not be served do not belong here.
RUN pip install -r requirements.txt

VOLUME data

CMD ["python", "on_startup.py"]
