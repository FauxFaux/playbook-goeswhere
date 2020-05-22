FROM buildpack-deps:20.04 AS build

RUN git clone -b unreal50 --depth 100 https://github.com/unrealircd/unrealircd/ && \
    cd unrealircd && \
    git checkout 893cc2db9988413a0f28d2d8da985997db069bea

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        libssl-dev \
        libargon2-dev \
        libpcre2-dev \
        pkg-config \
        libtre-dev \
    && apt-get clean

WORKDIR unrealircd

ADD config.settings .
RUN ./Config -quick

RUN make -j$(nproc) install

FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        bash \
        dumb-init \
        libargon2-1 \
        libssl1.1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists

RUN useradd --create-home --home-dir /srv/app app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

COPY --from=build --chown=app:app /opt /opt

USER app
CMD ["/opt/unreal/unrealircd", "start"]
