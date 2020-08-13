import faust

from simple_settings import settings

from aiocassandra import aiosession
from cassandra.cluster import Cluster

cluster = Cluster()

cassandra_session = cluster.connect()

aiosession(cassandra_session)

app = faust.App(
    id="weather-app",
    debug=settings.DEBUG,
    autodiscover=["weather"],
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
    store=settings.STORE_URI,
    logging_config=settings.LOGGING,
    topic_allow_declare=settings.TOPIC_ALLOW_DECLARE,
    topic_disable_leader=settings.TOPIC_DISABLE_LEADER,
    broker_credentials=settings.SSL_CONTEXT,
)
