# Dockerfile for the customized Pocket backend

FROM poktnetwork/pocket:RC-0.6.1

RUN apk add --update --no-cache expect bash leveldb-dev moreutils jq

RUN addgroup --gid 1001 -S app
RUN adduser --uid 1005 -S -G app app

RUN mkdir -p /home/app/.pocket/config
RUN chown -R app /home/app/.pocket/ /bin/pocket

USER app

ENTRYPOINT ["/bin/pocket", "start"]
