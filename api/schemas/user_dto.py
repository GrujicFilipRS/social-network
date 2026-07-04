from __future__ import annotations

from pydantic import BaseModel

from models import User

class UserDTO(BaseModel):
    id: str
    username: str
    name: str | None
    
    @staticmethod
    def to_dto(user: User) -> UserDTO:
        return UserDTO(
            id = str(user.id),
            username = user.username,
            name = user.name
        )