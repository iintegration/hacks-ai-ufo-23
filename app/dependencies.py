from typing import Annotated

from fastapi import Header, HTTPException

from app.database import edgedb_client
from app.queries.get_user_by_auth_data_async_edgeql import GetUserByAuthDataResult
from app.queries.get_user_by_token_async_edgeql import get_user_by_token, GetUserByTokenResult


async def verify_token(x_token: Annotated[str, Header()]) -> GetUserByTokenResult:
    user = await get_user_by_token(edgedb_client, token=x_token)
    if user is None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return user
