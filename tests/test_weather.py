import pytest

from weather.agents import verify_and_store
from weather.models import Weather

from unittest.mock import Mock, patch

import uuid

@pytest.mark.asyncio()
async def test_enrich_country_and_store(test_app):
    assert True
    # todo
    # async with verify_and_store.test_context() as agent:
    #     good_weather = Weather(
    #         id=str(uuid.uuid4()),
    #         occurred_at=123,
    #         lat=34.0522,
    #         long=118.2437,
    #         temperature_c=10
    #     )
    #     bad_weather = Weather(
    #         id=str(uuid.uuid4()),
    #         occurred_at=456,
    #         lat=34.0522,
    #         long=118.2437,
    #         temperature_c=100
    #     )
    #
    #     await agent.put(good_weather)
    #     await agent.put(bad_weather)
