ARG GOLANG_IMAGE_VERSION=golang:1.16.2-alpine3.13
FROM ${GOLANG_IMAGE_VERSION} AS builder

RUN apk -v --update --no-cache add \
	curl \
	git \
	groff \
	less \
	mailcap \
	gcc \
	libc-dev \
	bash  \
	leveldb-dev && \
	rm /var/cache/apk/* || true

ENV POCKET_PATH=/go/src/github.com/pokt-network/pocket-core/
ENV GO111MODULE="on"

RUN mkdir -p ${POCKET_PATH}

WORKDIR $POCKET_PATH

RUN git clone --branch staging https://github.com/pokt-network/pocket-core.git ${POCKET_PATH}
COPY 0.6.3.patch ${POCKET_PATH}
RUN cd ${POCKET_PATH} && git checkout RC-0.6.3 && git apply 0.6.3.patch
RUN go build -tags cleveldb -o ${GOBIN}/bin/pocket ./app/cmd/pocket_core/main.go

FROM alpine:3.13

COPY --from=builder /bin/pocket /bin/pocket

RUN apk add --update --no-cache expect bash leveldb-dev

RUN addgroup --gid 1001 -S app
RUN adduser --uid 1005 -S -G app app
RUN chown -R app /bin/pocket  && mkdir -p /home/app/.pocket/config
COPY config.json /home/app/.pocket/config/config.json

RUN chown -R app /home/app/.pocket

USER app
WORKDIR /home/app

ENTRYPOINT ["/bin/pocket", "start", "--mainnet", "--seeds", "03b74fa3c68356bb40d58ecc10129479b159a145@seed1.mainnet.pokt.network:20656,64c91701ea98440bc3674fdb9a99311461cdfd6f@seed2.mainnet.pokt.network:21656"]
