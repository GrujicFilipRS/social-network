from __future__ import annotations

from datetime import datetime
from uuid import UUID

from models import Notification
from pydantic import BaseModel

from ..user.user_dto import UserDTO


class NotificationDTO(BaseModel):
    id: UUID
    receiver: UserDTO
    sender: UserDTO
    object_type: str
    object_id: UUID
    seen: bool
    received_at: datetime
    
    def to_dto(notification: Notification | NotificationDTO) -> NotificationDTO:
        if isinstance(notification, NotificationDTO):
            return notification
        
        return NotificationDTO (
            id=notification.id,
            receiver=UserDTO.to_dto(notification.receiver),
            sender=UserDTO.to_dto(notification.sender),
            object_type=notification.object_type,
            object_id=notification.object_id,
            seen=notification.seen,
            received_at=notification.received_at
        )