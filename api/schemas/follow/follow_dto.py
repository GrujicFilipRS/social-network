from __future__ import annotations

from uuid import UUID

from models import Follow
from pydantic import BaseModel


class FollowDTO(BaseModel):
    id: UUID
    follower_id: UUID
    followed_id: UUID
    
    @staticmethod
    def to_dto(follow: Follow | FollowDTO) -> FollowDTO:
        if isinstance(follow, FollowDTO):
            return follow
        
        return FollowDTO(
            id = follow.id,
            follower_id = follow.follower_id,
            followed_id = follow.followed_id
        )