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
        message_txt = ''
        if notification.object_type == 'follow':
            message_txt = 'You have a new follower'
        elif notification.object_type == 'comment':
            message_txt = 'You have received a new comment.'
        elif notification.object_type == 'like':
            message_txt = 'Your post has been liked.'
        elif notification.object_type == 'post':
            message_txt = f'{notification.sender.username} has created a new post.'

        message = {
            'message_txt': message_txt,
            'object_type': notification.object_type,
            'object_id': str(notification.object_id)
        }
        
        return message
