# Dockerfile for the frontend Sandwalker

FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    libressl-dev \
    zlib-dev \
    jpeg-dev \
    g++

COPY infra/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

ADD app.py /code/
ADD sandwalker /code/sandwalker
ADD infra /code/infra

ENV FLASK_ENV_CONFIG=/code/infra/config-dev.cfg

CMD ["gunicorn", "-w", "4", "-b", ":5000", "app:app"]
