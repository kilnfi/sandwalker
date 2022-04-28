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
COPY 0.8.2.patch ${POCKET_PATH}
RUN cd ${POCKET_PATH} && git checkout RC-0.8.2 && git apply 0.8.2.patch
RUN go mod tidy
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
COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
