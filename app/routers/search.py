from fastapi import APIRouter

from app.database import edgedb_client
from app.queries.search_by_obj_key_async_edgeql import search_by_obj_key, SearchByObjKeyResult

router = APIRouter()


@router.get("/search/")
async def search(obj_key: str) -> list[SearchByObjKeyResult]:
    return await search_by_obj_key(edgedb_client, obj_key=obj_key)
