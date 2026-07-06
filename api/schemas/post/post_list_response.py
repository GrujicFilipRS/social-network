from __future__ import annotations

from models import Post
from ..shared.dto import DTO
from .post_dto import PostDTO

class PostListResponse(DTO):
    posts: list[PostDTO]
    
    @staticmethod
    def ok(posts: list[Post] | list[PostDTO], message: str | None = None) -> PostListResponse:
        if len(posts) == 0:
            return PostListResponse(
                success = True,
                message = message,
                posts = []
            )
        
        if isinstance(posts[0], Post):
            return PostListResponse(
                success = True,
                message = message,
                posts = [PostDTO.to_dto(p) for p in posts]
            )
        
        return PostListResponse(
            success = True,
            message = message,
            posts = posts
        )
    
    @staticmethod
    def error(message: str) -> PostListResponse:
        return PostListResponse(
            success = False,
            message = message,
            posts = []
        )