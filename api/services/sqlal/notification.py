from uuid import UUID

from schemas import NotificationGetResponse
from services.service_models import (
    NotificationModelServiceModel,
    NotificationServiceModel,
)
from sqlalchemy.orm import Session
from utils import ConnectionController


class NotificationServiceSqlal(NotificationServiceModel):
    def __init__(self, db_session: Session, notification_model_service: NotificationModelServiceModel):
        self.db_session = db_session
        self.notification_model_service = notification_model_service

    async def create_notification(
        self,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> NotificationGetResponse:
        notification_response = await self.notification_model_service.create_notification(
            receiver_id,
            sender_id,
            object_type,
            object_id
        )
        
        if not notification_response.success:
            return notification_response
        
        notification = notification_response.notification
        
        seen = await ConnectionController.send_to_user(
            receiver_id,
            dict(notification.to_dto())
        )
        
        if seen:
            await self.notification_model_service.read_notification(notification.id, receiver_id)
        
        return notification_response
        