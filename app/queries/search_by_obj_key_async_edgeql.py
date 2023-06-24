# AUTOGENERATED FROM 'app/queries/search_by_obj_key.edgeql' WITH:
#     $ edgedb-py -I hackathon --tls-security insecure --skip-pydantic-validation


from __future__ import annotations
import dataclasses
import datetime
import edgedb
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass

        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class SearchByObjKeyResult(NoPydanticValidation):
    created: datetime.datetime | None
    id: uuid.UUID
    modified: datetime.datetime | None
    obj_key: str
    state: str | None
    general_contractor: str | None
    general_designer_key: str | None
    number_of_workers: int | None
    square: str | None
    subtype: str | None
    type: str | None


async def search_by_obj_key(
    executor: edgedb.AsyncIOExecutor,
    *,
    obj_key: str,
) -> list[SearchByObjKeyResult]:
    return await executor.query(
        """\
        select Subject{*} filter .obj_key like <str>$obj_key ++ '%'\
        """,
        obj_key=obj_key,
    )
