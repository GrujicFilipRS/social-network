from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any
from uuid import uuid7

from db import SqlAlchemyBase
from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import User

class PFP(SqlAlchemyBase):
    __tablename__ = 'pfps'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid7
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False,
        unique=True
    )
    image_src: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    image_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    user: Mapped[User] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='pfp'
    )

    def to_dict(self, req_user: bool = False) -> dict[str, Any]:
        content: dict[str, Any] = {
            'id': str(self.id),
            'image_src': self.image_src,
            'image_id': self.image_id
        }

        if req_user:
            content['user'] = self.user.to_dict()
        
        return content