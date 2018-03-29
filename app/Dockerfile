FROM python:3.6.4-alpine3.7

WORKDIR /app

COPY requirements.txt .

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            linux-headers \
            musl-dev \
    && pip install -U pip \
    && pip install -r requirements.txt \
    && pip install uwsgi==2.0.17 \
    && find /usr/local \
            \( -type d -a -name test -o -name tests \) \
            -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            -exec rm -rf '{}' + \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
            )" \
    && rm requirements.txt \
    && apk add --no-cache --virtual .runtime-deps \
            $runDeps \ 
    && apk del .build-deps \
    && rm -rf /root/.cache /var/cache/apk/* /tmp/*

COPY src /app

ENV UWSGI_MODULE=main \
    UWSGI_CALLABLE=app \
    UWSGI_SOCKET=0.0.0.0:8000 \
    UWSGI_MASTER=1 \
    UWSGI_WORKERS=2 \
    UWSGI_THREADS=8 \
    UWSGI_LAZY_APPS=1


EXPOSE 8000

CMD ["uwsgi"] 
