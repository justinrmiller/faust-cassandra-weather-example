import faust


class Weather(faust.Record):
    id: str
    occurred_at: int
    lat: float
    long: float
    temperature_c: float
