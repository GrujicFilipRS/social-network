from __future__ import annotations
from dataclasses import dataclass

from models import User


@dataclass
class UserDTO:
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