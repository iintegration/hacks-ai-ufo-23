import os
from pathlib import Path
from typing import Annotated, Optional
from uuid import UUID

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, Form

from app import background
from app.database import edgedb_client
from app.dependencies import verify_token
from app.minio import minio_client
from app.models.file_created import FileCreated
from app.queries.add_file_async_edgeql import add_file
from app.queries.get_user_by_token_async_edgeql import GetUserByTokenResult
from app.settings import SETTINGS

router = APIRouter()


async def create_file(
    user: GetUserByTokenResult, uploaded_file: UploadFile, obj_key: Optional[str] = None
) -> UUID:
    database_file = await add_file(
        edgedb_client, user_id=user.id, origin_filename=uploaded_file.filename, obj_key=obj_key
    )
    file_location = f"files/{database_file.id}.xls"
    object_name = str(database_file.id)

    os.makedirs("files", exist_ok=True)

    async with aiofiles.open(file_location, "wb+") as temp:
        await temp.write(await uploaded_file.read())

    await minio_client.fput_object(
        bucket_name=SETTINGS.s3_bucket,
        object_name=object_name,
        file_path=file_location,
    )

    Path(file_location).unlink()
    return database_file.id


@router.post("/upload/{obj_key}/")
async def add_file_with_obj_key(
    uploaded_file: UploadFile,
    user: Annotated[GetUserByTokenResult, Depends(verify_token)],
    obj_key: str,
) -> FileCreated:
    object_id = await create_file(user=user, uploaded_file=uploaded_file, obj_key=obj_key)
    background.analyze_data.send(str(object_id))
    return FileCreated(id=object_id)


@router.post("/upload/")
async def add_upload_file(
    uploaded_file: UploadFile, user: Annotated[GetUserByTokenResult, Depends(verify_token)]
) -> FileCreated:
    object_id = await create_file(user=user, uploaded_file=uploaded_file)
    background.analyze_data.send(str(object_id))
    return FileCreated(id=object_id)
