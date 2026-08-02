from __future__ import annotations

import unicodedata
import uuid
from datetime import datetime
from typing import Any

from db import SqlAlchemyBase
from sqlalchemy import UUID, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .posts import Post
from .users import User


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4
    )
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=False
    )
    comment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey('comments.id'),
        nullable=True
    )
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )
    commented_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    post: Mapped[Post] = relationship(
        foreign_keys=[post_id],
        back_populates='comments'
    )
    comment: Mapped[Comment | None] = relationship(
        foreign_keys=[comment_id]
    )
    creator: Mapped[User] = relationship(
        foreign_keys=[creator_id],
        back_populates='comments'
    )

    def to_dict(self) -> dict[str, Any]:
        content: dict[str, Any] = {
            'id': str(self.id),
            'body': self.body,
            'post_id': str(self.post_id),
            'comment_id': str(self.comment_id) if self.comment_id else None,
            'creator': self.creator.to_dict(),
            'commented_at': str(self.commented_at)
        }
        
        return content
    
    @staticmethod
    def validate_body(data: Any) -> bool:
        body = data.get('body')
        
        if not body or not isinstance(body, str):
            return False

        body = body.strip()

        MIN_BODY_LENGTH = 1
        MAX_BODY_LENGTH = 80

        if len(body) < MIN_BODY_LENGTH or len(body) > MAX_BODY_LENGTH:
            return False

        MAX_BODY_LINES = 3
        if body.count('\n') > MAX_BODY_LINES:
            return False

        if not all(c.isprintable() or c in '\n\r\t' for c in body):
            return False

        DANGEROUS_SUBSTRINGS = (
            '<script',
            '</script',
            'javascript:',
            'onerror=',
            'onload=',
            '<iframe',
            '</iframe',
        )

        lower_body = body.lower()
        if any(x in lower_body for x in DANGEROUS_SUBSTRINGS):
            return False

        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in body
        ):
            return False
        
        return body.replace('\n', '').strip() != ''
    
    @staticmethod
    def validate_creation(data: dict[str, Any]) -> bool:
        post_id = data.get('post_id')
        comment_id = data.get('comment_id')
        
        if not Comment.validate_body(data):
            return False
        
        if not post_id or not isinstance(post_id, str):
            return False
        
        if comment_id and not isinstance(comment_id, str):
            return False
        
        try:
            uuid.UUID(post_id)
            uuid.UUID(comment_id) if comment_id else None
        except ValueError:
            return False
        
        return True