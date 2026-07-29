from __future__ import annotations

from datetime import datetime
from uuid import UUID

from models import Comment
from pydantic import BaseModel

from ..user.user_dto import UserDTO


class CommentDTO(BaseModel):
    id: UUID
    body: str
    post_id: UUID
    comment_id: UUID | None
    creator: UserDTO
    commented_at: datetime | None
    
    @staticmethod
    def to_dto(comment: CommentDTO | Comment) -> CommentDTO:
        if isinstance(comment, CommentDTO):
            return comment
        
        return CommentDTO(
            id = comment.id,
            body = comment.body,
            post_id = comment.post_id,
            comment_id = comment.comment_id,
            creator = comment.creator,
            commented_at = comment.commented_at
        )