from __future__ import annotations

from models import Comment

from ..shared.dto import DTO
from .comment_dto import CommentDTO


class CommentListResponse(DTO):
    comments: list[CommentDTO]
    
    @staticmethod
    def ok(comments: list[Comment] | list[CommentDTO], message: str | None = None) -> CommentListResponse:
        return CommentListResponse(
            success = True,
            message = message,
            comments = [ CommentDTO.to_dto(comment) for comment in comments ]
        )
    
    @staticmethod
    def error(message: str) -> CommentListResponse:
        return CommentListResponse(
            success = False,
            message = message,
            comments = []
        )