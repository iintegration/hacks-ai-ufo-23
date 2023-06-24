from pydantic import BaseModel


class Auth(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    token: str
