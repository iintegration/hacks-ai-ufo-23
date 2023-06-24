from typing import TYPE_CHECKING

from pydantic import AnyUrl, BaseSettings, RedisDsn

if TYPE_CHECKING:
    from pydantic.networks import Parts


class EdgedbDsn(AnyUrl):
    __slots__ = ()
    allowed_schemes = {"edgedb"}
    host_required = False

    @staticmethod
    def get_default_parts(parts: "Parts") -> "Parts":
        return {
            "domain": "localhost" if not (parts["ipv4"] or parts["ipv6"]) else "",
            "port": "5656",
            "path": "",
        }


class Settings(BaseSettings):
    edgedb_dsn: EdgedbDsn | None
    redis_dsn: RedisDsn
    salt: str = "$2b$12$hlqG1qm3BA5HUjeEj.HWPu"
    s3_host: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str


SETTINGS = Settings()
