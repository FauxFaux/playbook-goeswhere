FROM rust:1-buster AS build

RUN git clone https://github.com/FauxFaux/quad-image && \
    cd quad-image && \
    git checkout 8820605f5ce5fec378b120ffdac6f0c8ce64f4f2

WORKDIR quad-image

RUN cargo fetch
RUN cargo build --release

FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        dumb-init \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists

RUN useradd --create-home --home-dir /srv/app app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

COPY --from=build /quad-image/target/release/quad-image /bin/quad-image

USER app
WORKDIR /srv/app
CMD ["/bin/quad-image"]
