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
            f'New notification from {sender_id} regarding {object_type} {object_id}'
        )
        
        return notification