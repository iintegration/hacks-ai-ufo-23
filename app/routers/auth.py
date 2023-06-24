import secrets
from typing import Annotated
from uuid import UUID

import bcrypt
from edgedb import ConstraintViolationError
from fastapi import APIRouter, Depends, HTTPException

from app.database import edgedb_client
from app.dependencies import verify_token
from app.models.auth import Auth, Token
from app.queries.add_token_async_edgeql import add_token
from app.queries.add_user_async_edgeql import add_user
from app.queries.delete_token_async_edgeql import delete_token
from app.queries.get_user_by_auth_data_async_edgeql import get_user_by_auth_data
from app.queries.get_user_by_token_async_edgeql import GetUserByTokenResult
from app.settings import SETTINGS

router = APIRouter()


async def generate_token(user_id: UUID) -> str:
    token = secrets.token_urlsafe(128)
    while True:
        try:
            await add_token(edgedb_client, user_id=user_id, token=token)
        except ConstraintViolationError:
            continue
        else:
            return token


@router.post("/auth/")
async def auth(auth_data: Auth) -> Token:
    password = auth_data.password.encode()
    hashed = bcrypt.hashpw(password, SETTINGS.salt.encode()).decode()
    user = await get_user_by_auth_data(edgedb_client, login=auth_data.login, password_hash=hashed)
    if user is None:
        raise HTTPException(status_code=400, detail="username or password invalid")

    token = await generate_token(user_id=user.id)
    return Token(token=token)


@router.post("/register/")
async def register(auth_data: Auth) -> Token:
    password = auth_data.password.encode()
    hashed = bcrypt.hashpw(password, SETTINGS.salt.encode()).decode()
    try:
        user = await add_user(edgedb_client, login=auth_data.login, password_hash=hashed)
    except ConstraintViolationError as error:
        raise HTTPException(status_code=400, detail="username already taken") from error

    token = await generate_token(user_id=user.id)
    return Token(token=token)


@router.post("/logout/")
async def logout(current_user: Annotated[GetUserByTokenResult, Depends(verify_token)]) -> bool:
    await delete_token(edgedb_client, token=current_user.token)
    return True
