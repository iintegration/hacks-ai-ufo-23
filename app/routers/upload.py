import os
import shutil
from typing import Annotated

import aiofiles
from fastapi import APIRouter, UploadFile, Depends

from app.database import edgedb_client
from app.dependencies import verify_token
from app.queries.add_file_async_edgeql import add_file
from app.queries.get_user_by_token_async_edgeql import GetUserByTokenResult

router = APIRouter()


@router.post("/upload/")
async def create_upload_file(uploaded_file: UploadFile, user: Annotated[GetUserByTokenResult, Depends(verify_token)]):
    database_file = await add_file(edgedb_client, user_id=user.id)
    file_location = f"files/{database_file.id}.xls"

    async with aiofiles.open(file_location, "wb") as temp:
        await temp.write(await uploaded_file.read())

    os.remove(file_location)
