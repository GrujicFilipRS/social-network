from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid7

from db import SqlAlchemyBase
from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import User

class Follow(SqlAlchemyBase):
    __tablename__ = 'follows'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid7
    )
    followed_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    follower_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )
    followed_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False
    )

    follower: Mapped[User] = relationship(
        'User',
        foreign_keys=[follower_id],
        back_populates='follows'
    )
    followed: Mapped[User] = relationship(
        'User',
        foreign_keys=[followed_id],
        back_populates='followers'
    )

    def to_dict(self, req_names: bool = False) -> dict[str, Any]:
        data: dict[str, Any] = {
            'id': str(self.id),
            'followed_at': str(self.followed_datetime)
        }

        if req_names:
            data['follower'] = self.follower.to_dict()
            data['followed'] = self.followed.to_dict()
        else:
            data['follower_id'] = str(self.follower_id)
            data['followed_id'] = str(self.followed_id)
        
        return data