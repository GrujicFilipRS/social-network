from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel

from models import Post

class PostDTO(BaseModel):
    id: str
    title: str
    body: str | None
    status: str
    created_at: datetime
    
    @staticmethod
    def to_dto(post: Post | PostDTO) -> PostDTO:
        if isinstance(post, PostDTO):
            return post
        
        return PostDTO(
            id = str(post.id),
            title = post.title,
            body = post.body,
            status = post.status,
            created_at = post.created_at
        )