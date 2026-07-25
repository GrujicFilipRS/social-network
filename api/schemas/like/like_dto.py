from __future__ import annotations

from datetime import datetime
from uuid import UUID

from models import Like
from pydantic import BaseModel


class LikeDTO(BaseModel):
    user_id: UUID
    post_id: UUID
    liked_at: datetime | None
    
    @staticmethod
    def to_dto(like: Like | LikeDTO) -> LikeDTO:
        if isinstance(like, LikeDTO):
            return like
        
        return LikeDTO(
            user_id = like.user_id,
            post_id = like.post_id,
            liked_at = like.liked_at
        )