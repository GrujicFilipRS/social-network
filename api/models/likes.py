from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
import uuid
from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db import SqlAlchemyBase

if TYPE_CHECKING:
    from models import User, Post

class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )
    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=False
    )
    liked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='likes'
    )
    post: Mapped['Post'] = relationship(
        'Post',
        foreign_keys=[post_id],
        back_populates='likes'
    )

    def to_dict(self) -> dict[str, Any]:
        content: dict[str, Any] = {
            'id': str(self.id),
            'post': self.post.to_dict(),
            'user': self.user.to_dict(),
            'liked_at': str(self.liked_at)
        }

        return content