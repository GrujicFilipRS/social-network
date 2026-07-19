from __future__ import annotations

from .like_dto import LikeDTO
from ..shared.dto import DTO

from models import Like


class LikeGetResponse(DTO):
    like: LikeDTO | None
    
    @staticmethod
    def ok(like: Like | LikeDTO, message: str | None = None) -> LikeGetResponse:
        return LikeGetResponse(
            success = True,
            message = message,
            like = LikeDTO.to_dto(like)
        )
    
    @staticmethod
    def error(message: str) -> LikeGetResponse:
        return LikeGetResponse(
            success = False,
            message = message,
            like = None
        )