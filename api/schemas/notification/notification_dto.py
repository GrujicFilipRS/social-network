from __future__ import annotations

from models import Notification
from pydantic import BaseModel


class NotificationDTO(BaseModel): # TODO
    def to_dto(notification: Notification) -> NotificationDTO:
        return NotificationDTO()