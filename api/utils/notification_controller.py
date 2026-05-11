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
        session.flush()
        
        seen = await ConnectionController.send_to_user_if_connected(
            receiver_id,
            NotificationController.generate_notification_message(notification)
        )
        
        notification.seen = seen
        session.commit()
        
        return notification
    
    @staticmethod
    def generate_notification_message(notification: Notification) -> dict[str, Any]:
        sender_name: str = (
            notification.sender.name
            if notification.sender.name
            else notification.sender.username
        )
        message_txt = ''
        
        if notification.object_type == 'follow':
            message_txt = f'{sender_name} is now following you.'
        elif notification.object_type == 'comment':
            message_txt = f'{sender_name} has commented on your post.'
        elif notification.object_type == 'like':
            message_txt = f'{sender_name} has liked your post.'
        elif notification.object_type == 'post':
            message_txt = f'{sender_name} has posted.'

        message = {
            'message_txt': message_txt,
            'object_type': notification.object_type,
            'object_id': str(notification.object_id)
        }
        
        return message
