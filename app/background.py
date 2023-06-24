import dramatiq
from dramatiq.brokers.redis import RedisBroker
from edgedb import create_client

from app.settings import SETTINGS


redis_broker = RedisBroker(url=SETTINGS.redis_dsn)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def analyze_data(object_name: str):
    print(object_name)
