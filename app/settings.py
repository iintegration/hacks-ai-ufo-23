from typing import Optional

from pydantic import BaseSettings, RedisDsn, AnyUrl, SecretStr


class EdgedbDsn(AnyUrl):
    __slots__ = ()
    allowed_schemes = {"edgedb"}
    host_required = False

    @staticmethod
    def get_default_parts(parts: "Parts") -> "Parts":
        return {
            "domain": "localhost" if not (parts["ipv4"] or parts["ipv6"]) else "",
            "port": "5656",
            "path": "/0",
        }


class Settings(BaseSettings):
    edgedb_dsn: Optional[EdgedbDsn]
    redis_dsn: RedisDsn = "redis://user:pass@localhost:6379/1"
    salt: SecretStr = SecretStr("$2b$12$hlqG1qm3BA5HUjeEj.HWPu")
    s3_host: str
    s3_access_key: SecretStr
    s3_secret_key: SecretStr
    s3_bucket: str


SETTINGS = Settings()
