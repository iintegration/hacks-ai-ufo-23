# AUTOGENERATED FROM 'app/queries/get_subjects.edgeql' WITH:
#     $ edgedb-py


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
class GetSubjectsResult(NoPydanticValidation):
    created: datetime.datetime | None
    obj_key: str
    state: str | None
    id: uuid.UUID
    modified: datetime.datetime | None
    general_contractor: str | None
    general_designer_key: str | None
    number_of_workers: int | None
    square: str | None
    subtype: str | None
    type: str | None
    photo_url: str | None


async def get_subjects(
    executor: edgedb.AsyncIOExecutor,
    *,
    offset: int | None,
    limit: int | None,
) -> list[GetSubjectsResult]:
    return await executor.query(
        """\
        select Subject{*} offset <optional int64>$offset limit <optional int64>$limit\
        """,
        offset=offset,
        limit=limit,
    )