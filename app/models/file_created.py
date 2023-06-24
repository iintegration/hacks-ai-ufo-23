from uuid import UUID

from pydantic import BaseModel


class FileCreated(BaseModel):
    id: UUID
