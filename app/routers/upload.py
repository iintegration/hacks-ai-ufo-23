from pathlib import Path
from typing import Annotated

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


@router.post("/upload/")
async def create_upload_file(
    uploaded_file: UploadFile,
    user: Annotated[GetUserByTokenResult, Depends(verify_token)],
    obj_key: Annotated[str, Form()],
) -> FileCreated:
    database_file = await add_file(
        edgedb_client,
        user_id=user.id,
        origin_filename=uploaded_file.filename,
        obj_key=obj_key
    )
    file_location = f"files/{database_file.id}.xls"
    object_name = str(database_file.id)

    Path("files").mkdir(parents=True)

    async with aiofiles.open(file_location, "wb+") as temp:
        await temp.write(await uploaded_file.read())

    await minio_client.fput_object(
        bucket_name=SETTINGS.s3_bucket,
        object_name=object_name,
        file_path=file_location,
    )

    Path(file_location).unlink()
    background.analyze_data.send(object_name)
    return FileCreated(id=database_file.id)
