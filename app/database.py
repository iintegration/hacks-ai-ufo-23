import edgedb

from app.settings import SETTINGS

edgedb_client = edgedb.create_async_client(dsn=SETTINGS.edgedb_dsn, tls_security="insecure")
