from __future__ import annotations

from models import User
from ..shared.dto import DTO
from .user_dto import UserDTO

class UserGetResponse(DTO):
    user: UserDTO | None
    
    @staticmethod
    def ok(user: User, message: str | None = None) -> UserGetResponse:
        return UserGetResponse(
            success = True,
            message = message,
            user = UserDTO.to_dto(user)
        )
    
    @staticmethod
    def error(message: str) -> UserGetResponse:
        return UserGetResponse(
            success = False,
            message = message,
            user = None
        )