from miniopy_async import Minio

from app.settings import SETTINGS

client = Minio(
    SETTINGS.s3_host,
    access_key=SETTINGS.s3_access_key,
    secret_key=SETTINGS.s3_secret_key,
    secure=False
)
