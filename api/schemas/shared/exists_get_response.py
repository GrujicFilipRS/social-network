from __future__ import annotations

from .dto import DTO

class ExistsGetResponse(DTO):
    exists: bool
    
    @staticmethod
    def ok(exists: bool, message: str | None = None) -> ExistsGetResponse:
        return ExistsGetResponse(
            success = True,
            message = message,
            exists = exists
        )
    
    @staticmethod
    def error(message: str) -> ExistsGetResponse:
        return ExistsGetResponse(
            success = False,
            message = message,
            exists = False
        )