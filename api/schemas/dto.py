from __future__ import annotations

from dataclasses import dataclass

@dataclass
class DTO:
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