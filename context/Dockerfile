FROM python:2.7.13

WORKDIR /var/www
COPY . .
# TODO: Files which will not be served do not belong here.
RUN pip install -r requirements.txt

# TODO
#RUN groupadd -r www && useradd -r -g www www
#RUN chown www:www .
#USER www

RUN python -m wget http://igv.org/web/release/1.0.7/igv-1.0.7.js
RUN python -m wget http://igv.org/web/release/1.0.7/igv-1.0.7.css

RUN python -m wget http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js
RUN python -m wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css
RUN python -m wget http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js

VOLUME data

CMD ["python", "on_startup.py"]
