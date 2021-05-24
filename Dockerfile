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

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

ADD app.py /code/
ADD sandwalker /code/sandwalker

ENV DATABASE_URI "sqlite:///../infra/data/timeline.db"

CMD ["gunicorn", "-w", "4", "-b", ":5000", "app:app"]
