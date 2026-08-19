from __future__ import annotations

from models import Follow

from ..shared import DTO
from .follow_dto import FollowDTO


class FollowGetResponse(DTO):
    follow: FollowDTO | None
    
    @staticmethod
    def ok(follow: FollowDTO | Follow, message: str | None = None) -> FollowGetResponse:
        return FollowGetResponse(
            success=True,
            message=message,
            follow=FollowDTO.to_dto(follow)
        )
    
    @staticmethod
    def error(message: str) -> FollowGetResponse:
        return FollowGetResponse(
            success=False,
            message=message,
            follow=None
        )