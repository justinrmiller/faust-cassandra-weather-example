Faust Cassandra Weather Example
===============================

This project is meant to demonstrate the capabilities of Faust and aiocassandra.

For getting started with your own Faust project, I recommend also checking out the Faust cookiecutter project worked on by Marcos Schroh:

https://github.com/marcosschroh/cookiecutter-faust

:License: MIT

Installation
------------

Install local requirements:

```bash
make install
```

Usage
------

If you do not have a cluster running locally you can use `docker-compose` to avoid several headaches.
By default:
- `KAFKA_BOOTSTRAP_SERVER` is `kafka://localhost:29092`.

```bash
make start-infra
```

Wait for a moment for the whole infrastructure to spin up.

Create Kafka Topics:
```bash
./scripts/create-topics
```

Create Cassandra Tables:
```bash
./scripts/create-tables
```

Then, start the example:

```bash
make start-app
```

Settings
--------

Settings are created based on [local-settings](https://github.com/drgarcia1986/simple-settings) package.

The only settings required if the `KAFKA_BOOTSTRAP_SERVER` environment variable.

```python
SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True,
    'REQUIRED_SETTINGS': ('KAFKA_BOOTSTRAP_SERVER', 'STORE_URI'),
}

# The following variables can be ovirriden from ENV
KAFKA_BOOTSTRAP_SERVER = "kafka://localhost:29092"

TOPIC_ALLOW_DECLARE = True
TOPIC_DISABLE_LEADER = False

SSL_ENABLED = False
SSL_CONTEXT = None

if SSL_ENABLED:
    # file in pem format containing the client certificate, as well as any ca certificates
    # needed to establish the certificate’s authenticity
    KAFKA_SSL_CERT = None

    # filename containing the client private key
    KAFKA_SSL_KEY = None

    # filename of ca file to use in certificate verification
    KAFKA_SSL_CABUNDLE = None

    # password for decrypting the client private key
    SSL_KEY_PASSWORD = None

    SSL_CONTEXT = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=KAFKA_SSL_CABUNDLE)

    SSL_CONTEXT.load_cert_chain(KAFKA_SSL_CERT, keyfile=KAFKA_SSL_KEY, password=SSL_KEY_PASSWORD)
```

The settings also include a basic logging configuration:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'weather': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

Basic Commands
--------------

* Start application: `make kafka-cluster`. Note: This command also starts the weather application.
* Stop and remove containers: `make stop-kafka-cluster`
* Install requirements: `make install`
* Start Faust application: `make start-app`
* List topics: `make list-topics`
* Create weather topic: `make create-topic topic-name="weather"`
* List agents: `make list-agents`
* Send events to weather topic/agent: `make send-weather-event payload='{"id": "c97a5c79-fb8d-4b07-9686-61ec62eb12d4", "occurred_at": 1597342944704, "lat": 12.0, "long": 45.0, "temperature_c": 25.0}'`

Docker
------

The `Dockerfile` is based on  `python:3.7-slim`.

Docker Compose
--------------

`docker-compose.yaml` includes `zookeeper` and `kafka` based on `confluent-inc`.
For more information you can go to [confluentinc](https://docs.confluent.io/current/installation/docker/docs/index.html) and see the docker compose example [here](https://github.com/confluentinc/cp-docker-images/blob/master/examples/cp-all-in-one/docker-compose.yml#L23-L48)

Useful ENVIRONMENT variables that you may change:

|Variable| description  | example |
|--------|--------------|---------|
| WORKER_PORT | Worker port | `6066` |
| KAFKA_BOOTSTRAP_SERVER | Kafka servers | `kafka://localhost:29092` |
| KAFKA_BOOTSTRAP_SERVER_NAME | Kafka server name| `kafka` |
| KAFKA_BOOTSTRAP_SERVER_PORT | Kafka server port | `29092` |
| CASSANDRA_SERVER_NAME | Cassandra server name| `cassandra` |
| CASSANDRA_SERVER_PORT | Cassandra server port | `9042` |
| SCHEMA_REGISTRY_SERVER | Schema registry server name | `schema-registry` |
| SCHEMA_REGISTRY_SERVER_PORT | Schema registry server port | `8081` |
| SCHEMA_REGISTRY_URL | Schema Registry Server url | `http://schema-registry:8081` |

Run tests
---------

```sh
make install-tests
```

```sh
./scripts/test.sh
```

Lint code
---------

```sh
./scripts/lint
```

Type checks
-----------

Running type checks with mypy:

```sh
mypy faust-cassandra-weather-example
```
