from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session

from models import Notification
from .connection_controller import ConnectionController

class NotificationController:
    '''
    Controller class for handling creation of notifications
    and communication with the notification microservice.
    '''
    
    @staticmethod
    async def create_notification(
        session: Session,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> Notification:
        notification = Notification(
            receiver_id=receiver_id,
            sender_id=sender_id,
            object_type=object_type,
            object_id=object_id
        )
        session.add(notification)
        session.commit()
        
        await ConnectionController.send_to_user_if_connected(
            receiver_id,
            NotificationController.generate_notification_message(notification)
        )
        
        return notification
    
    @staticmethod
    def generate_notification_message(notification: Notification) -> dict[str, Any]:
        message = {
            'message_txt': f'You have a new notification from {notification.sender.username}',
            'object_type': notification.object_type,
            'object_id': str(notification.object_id)
        }
        
        return message
