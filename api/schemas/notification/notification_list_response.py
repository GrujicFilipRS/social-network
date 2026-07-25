from __future__ import annotations

from models import Notification

from ..shared.dto import DTO
from .notification_dto import NotificationDTO


class NotificationListResponse(DTO):
    notifications: list[NotificationDTO]
    
    @staticmethod
    def ok(
        notifications: list[Notification] | list[NotificationDTO],
        message: str | None = None
    ) -> NotificationListResponse:
        if len(notifications) == 0:
            return NotificationListResponse(
                success = True,
                message = message,
                notifications = []
            )
        
        if isinstance(notifications[0], Notification):
            return NotificationListResponse(
                success = True,
                message = message,
                notifications = [NotificationDTO.to_dto(n) for n in notifications]
            )
        
        return NotificationListResponse(
            success = True,
            message = message,
            notifications = notifications
        )
    
    @staticmethod
    def error(message: str) -> NotificationListResponse:
        return NotificationListResponse(
            success = False,
            message = message,
            notifications = []
        )