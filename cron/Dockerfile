# Dockerfile for the daily database dump

FROM python:3.7-alpine

RUN apk add --no-cache \
    sqlite

COPY dump /etc/periodic/daily/dump

CMD ["crond", "-l", "2", "-f"]
