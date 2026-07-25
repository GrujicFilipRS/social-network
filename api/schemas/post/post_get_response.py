from __future__ import annotations

from models import Post

from ..shared.dto import DTO
from .post_dto import PostDTO


class PostGetResponse(DTO):
    post: PostDTO | None
    
    @staticmethod
    def ok(post: Post, message: str | None = None) -> PostGetResponse:
        return PostGetResponse(
            success = True,
            message = message,
            post = PostDTO.to_dto(post)
        )
    
    @staticmethod
    def error(message: str) -> PostGetResponse:
        return PostGetResponse(
            success = False,
            message = message,
            post = None
        )