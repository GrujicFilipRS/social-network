from __future__ import annotations

from models import Follow

from ..shared.dto import DTO
from .follow_dto import FollowDTO


class FollowListResponse(DTO):
    follows: list[FollowDTO]
    
    @staticmethod
    def ok(follows: list[Follow] | list[FollowDTO], message: str | None = None) -> FollowListResponse:
        return FollowListResponse(
            success = True,
            message = message,
            follows = [FollowDTO.to_dto(f) for f in follows]
        )
    
    @staticmethod
    def error(message: str | None = None):
        return FollowListResponse(
            success = False,
            message = message,
            follows = []
        )