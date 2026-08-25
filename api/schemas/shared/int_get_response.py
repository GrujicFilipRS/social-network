from __future__ import annotations

from .dto import DTO


class IntegerGetResponse(DTO):
    number: int
    
    @staticmethod
    def ok(number: int, message: str | None = None) -> IntegerGetResponse:
        return IntegerGetResponse(
            success = True,
            message = message,
            number = number
        )
    
    @staticmethod
    def error(message: str) -> IntegerGetResponse:
        return IntegerGetResponse(
            success = False,
            message = message,
            number = 0
        )