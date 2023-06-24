from uuid import UUID

from fastapi import APIRouter, Depends

from app.database import edgedb_client
from app.dependencies import verify_token
from app.queries.get_tasks_async_edgeql import GetTasksResult, get_tasks

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("/subjects/{subject_id}/tasks/")
async def read_tasks(subject_id: UUID) -> list[GetTasksResult]:
    return await get_tasks(edgedb_client, subject_id=subject_id)
