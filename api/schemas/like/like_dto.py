from __future__ import annotations

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from models import Like


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