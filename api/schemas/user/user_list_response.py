from __future__ import annotations

from models import User

from ..shared.dto import DTO
from .user_dto import UserDTO


class UserListResponse(DTO):
    users: list[UserDTO]
    
    @staticmethod
    def ok(users: list[User] | list[UserDTO], message: str | None = None) -> UserListResponse:
        return UserListResponse(
            success = True,
            message = message,
            users = [UserDTO.to_dto(u) for u in users]
        )
    
    @staticmethod
    def error(message: str | None = None) -> UserListResponse:
        return UserListResponse(
            success = False,
            message = message,
            users = []
        )