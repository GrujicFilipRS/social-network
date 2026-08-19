from __future__ import annotations

from models import Notification

from ..shared.dto import DTO
from .notification_dto import NotificationDTO


class NotificationGetResponse(DTO):
    notification: NotificationDTO | None
    
    @staticmethod
    def ok(notification: Notification | NotificationDTO, message: str | None = None) -> NotificationGetResponse:
        return NotificationGetResponse(
            success=True,
            message=message,
            notification=NotificationDTO.to_dto(notification)
        )
    
    @staticmethod
    def error(message: str) -> NotificationGetResponse:
        return NotificationGetResponse(
            success=False,
            message=message,
            notification=None
        )