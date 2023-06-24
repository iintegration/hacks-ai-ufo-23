import dramatiq
from edgedb import create_client

from app.settings import SETTINGS

edgedb_client = create_client(dsn=SETTINGS.edgedb_dsn)


@dramatiq.actor
def analyse_data(url: str):
    pass
