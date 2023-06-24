from typing import Annotated

from fastapi import Header, HTTPException

from app.database import edgedb_client
from app.queries.get_user_by_token_async_edgeql import GetUserByTokenResult, get_user_by_token


async def verify_token(authorization: Annotated[str, Header()]) -> GetUserByTokenResult:
    user = await get_user_by_token(edgedb_client, token=authorization)
    if user is None:
        raise HTTPException(status_code=400, detail="Authorization header invalid")
    return user
