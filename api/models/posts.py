from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid7

from db import SqlAlchemyBase
from sqlalchemy import UUID, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import Comment, Like, Photo, User


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid7
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )

    user: Mapped[User] = relationship(
        'User',
        back_populates='posts'
    )
    likes: Mapped[list[Like]] = relationship(
        'Like',
        back_populates='post',
        cascade='all, delete-orphan'
    )
    comments: Mapped[list[Comment]] = relationship(
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan'
    )
    photos: Mapped[list[Photo]] = relationship(
        'Photo',
        back_populates='post',
        cascade='all, delete-orphan'
    )

    def to_dict(
        self,
        req_likes: bool = False,
        req_comments: bool = False
    ) -> dict[str, Any]:
        output: dict[str, Any] = {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'status': self.status,
            'user': self.user.to_dict(req_name=True),
            'photos': [ photo.to_dict() for photo in self.photos ],
            'created_at': self.created_at.strftime('%d. %m. %Y. %H:%M')
        }
        
        if req_likes:
            output['likes'] = len(self.likes)
        
        if req_comments:
            output['comments'] = [ comment.to_dict() for comment in self.comments ]
        
        return output

    def set_title(self, title: str) -> None:
        self.title = title
    
    def set_body(self, body: str) -> None:
        self.body = body
    
    def set_status(self, status: str) -> None:
        self.status = status