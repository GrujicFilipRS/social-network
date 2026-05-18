from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Text, UUID
from sqlalchemy.orm import Mapped, Session, relationship, mapped_column
from db import SqlAlchemyBase
from models import Like, Comment, Post, Follow

if TYPE_CHECKING:
    from models import User


class Notification(SqlAlchemyBase):
    __tablename__ = 'notifications'
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    receiver_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )
    object_type: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    object_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    received_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    seen: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    receiver: Mapped['User'] = relationship(
        'User',
        foreign_keys=[receiver_id]
    )
    sender: Mapped['User'] = relationship(
        'User',
        foreign_keys=[sender_id]
    )

    def get_object(self, session: Session) -> Like | Comment | Post | Follow | None:
        if self.object_type == 'like':
            return session.get(Like, self.object_id)
        
        elif self.object_type == 'comment':
            return session.get(Comment, self.object_id)
        
        elif self.object_type == 'post':
            return session.get(Post, self.object_id)
        
        elif self.object_type == 'follow':
            return session.get(Follow, self.object_id)
        
        return None

    def to_dict(self) -> dict[str, str]:
        sender_name: str = (
            self.sender.name
            if self.sender.name
            else self.sender.username
        )
        message_txt = ''
        
        if self.object_type == 'follow':
            message_txt = f'{sender_name} is now following you.'
        elif self.object_type == 'comment':
            message_txt = f'{sender_name} has commented on your post.'
        elif self.object_type == 'like':
            message_txt = f'{sender_name} has liked your post.'
        elif self.object_type == 'post':
            message_txt = f'{sender_name} has posted.'

        return {
            'id': str(self.id),
            'message_txt': message_txt,
            'object_type': self.object_type,
            'object_id': str(self.object_id),
            'received_at': self.received_at.isoformat() if self.received_at else ''
        }