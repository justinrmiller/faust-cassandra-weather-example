import asyncio
import datetime
import json
import logging
import math
import random
import uuid

from faust import current_event

from cassandra import ConsistencyLevel

from cassandra.query import SimpleStatement

from app import app, cassandra_session

from .models import Weather

weather_input_topic = app.topic("weather-input", value_type=Weather)
weather_accepted_topic = app.topic("weather-accepted", value_type=Weather)
weather_rejected_topic = app.topic("weather-rejected", value_type=Weather)

logger = logging.getLogger(__name__)

# temperature range above/below which we reject records
MIN_C = -88.0
MAX_C = 55.0


def generate_weather_insert_statement(weather):
    query = f'INSERT INTO demo.weather (' \
        f'id, occurred_at, lat, long, temperature_c'\
        f') VALUES (' \
        f'{weather.id}, {weather.occurred_at}, ' \
        f'{weather.lat}, {weather.long}, ' \
        f'{weather.temperature_c}' \
        f')'
    return query


def get_current_time_utc():
    epoch = datetime.datetime.utcfromtimestamp(0)
    return math.floor((datetime.datetime.utcnow() - epoch).total_seconds() * 1000.0)


@app.page('/count/')
async def get_count(self, request):
    # note: this is not advisable to do in production but is a useful example
    query = "SELECT count(*) from demo.weather;"

    result = await cassandra_session.execute_future(
        SimpleStatement(query, consistency_level=ConsistencyLevel.ONE)
    )

    return self.json({
        'count': result[0][0],
    })


@app.agent(weather_input_topic)
async def verify_and_store(weather_stream):
    async for weather in weather_stream:
        accepted = MIN_C < weather.temperature_c < MAX_C

        logger.info(f"Verify: Weather (accepted: {accepted}): {weather}")

        event = current_event()
        if accepted:
            query = generate_weather_insert_statement(weather)

            cassandra_future = cassandra_session.execute_future(
                SimpleStatement(query, consistency_level=ConsistencyLevel.ONE)
            )
            event_forward_future = event.forward(weather_accepted_topic)

            await asyncio.gather(cassandra_future, event_forward_future)
        else:
            await event.forward(weather_rejected_topic)


# emit messages_per_batch messages every 3 seconds
@app.timer(interval=3)
async def producer():
    messages_per_batch = 5

    logger.info(f"Processing batch of {messages_per_batch}")

    for i in range(messages_per_batch):
        message = {
            "id": str(uuid.uuid4()),
            "occurred_at": get_current_time_utc(),
            "lat": 34.0522,
            "long": 118.2437,
            "temperature_c": random.uniform(-150, 150)
        }

        await weather_input_topic.send(
            key=str(uuid.uuid4()),
            value=json.dumps(message).encode('ascii')
        )


@app.agent(weather_accepted_topic)
async def consume_accepted(weather_stream):
    async for weather in weather_stream:
        logger.info(f"Accept: {weather}")


@app.agent(weather_rejected_topic)
async def consume_rejected(weather_stream):
    async for weather in weather_stream:
        logger.info(f"Reject: {weather}")

