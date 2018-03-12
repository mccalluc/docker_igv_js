FROM python:2.7.13-alpine

WORKDIR /var/www
COPY . .
# TODO: Files which will not be served do not belong here.
RUN pip install -r requirements.txt

# TODO
#RUN groupadd -r www && useradd -r -g www www
#RUN chown www:www .
#USER www

ENV IGV_V=1.0.8
ENV IGV_BASE=http://igv.org/web/release/$IGV_V

# Download versioned igv to generic filenames so our index.html doesn't
# have to be updated
RUN python -m wget $IGV_BASE/igv-$IGV_V.js -o igv.js
RUN python -m wget $IGV_BASE/igv-$IGV_V.css -o igv.css

RUN mkdir img
WORKDIR img
RUN python -m wget $IGV_BASE/img/igv_logo_letters_paths.svg
RUN python -m wget $IGV_BASE/img/cursor_logo.svg
RUN python -m wget $IGV_BASE/img/cursor_logo.png
WORKDIR ..

ENV CDN_BASE=http://ajax.googleapis.com/ajax/libs
RUN python -m wget $CDN_BASE/jquery/1.11.1/jquery.min.js
RUN python -m wget $CDN_BASE/jqueryui/1.11.2/themes/smoothness/jquery-ui.css
RUN python -m wget $CDN_BASE/jqueryui/1.11.2/jquery-ui.min.js

VOLUME data

CMD ["python", "on_startup.py"]
