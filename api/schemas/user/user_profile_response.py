from __future__ import annotations

from models import User

from ..post.post_dto import PostDTO
from ..shared.dto import DTO
from .user_dto import UserDTO


class UserProfileResponse(DTO):
    user: UserDTO | None
    num_followers: int | None
    num_follows: int | None
    user_followed: bool | None
    posts: list[PostDTO]
    
    @staticmethod
    def ok(
        user: User,
        user_followed: bool,
        num_followers: int,
        num_follows: int,
        posts: list[PostDTO],
        message: str | None = None
    ) -> UserProfileResponse:
        return UserProfileResponse(
            success = True,
            message = message,
            user = UserDTO.to_dto(user),
            user_followed = user_followed,
            num_followers = num_followers,
            num_follows = num_follows,
            posts = posts
        )
    
    @staticmethod
    def error(message: str) -> UserProfileResponse:
        return UserProfileResponse(
            success = False,
            message = message,
            user = None,
            user_followed = False,
            num_followers = None,
            num_follows = None,
            posts = []
        )