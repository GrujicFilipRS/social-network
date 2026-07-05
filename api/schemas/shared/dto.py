from __future__ import annotations

from pydantic import BaseModel

class DTO(BaseModel):
    success: bool
    message: str | None
    
    @staticmethod
    def ok(message: str | None = None) -> DTO:
        return DTO(
            success = True,
            message = message
        )
    
    @staticmethod
    def error(message: str) -> DTO:
        return DTO(
            success = False,
            message = message
        )