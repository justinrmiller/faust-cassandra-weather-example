
FROM marcosschroh/rocksdb:0.0.1

RUN apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y netcat && apt-get autoremove -y \
    && apt-get install gcc make g++ libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev -y



ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /faust-cassandra-weather-example/

COPY . /faust-cassandra-weather-example

RUN make install-production


RUN yes Y | apt-get remove --purge git libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev


# Create unprivileged user
RUN groupadd --non-unique --gid 1000 faust && adduser --disabled-password --uid 1000 --gid 1000 faust
RUN chown -R faust:faust /faust-cassandra-weather-example
USER faust

ENTRYPOINT ["./scripts/run"]
