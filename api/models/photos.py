from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from uuid import uuid4

from db import SqlAlchemyBase
from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import Post

class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('posts.id', ondelete='CASCADE'),
        nullable=False
    )
    post_position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    image_src: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    image_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    post: Mapped[Post] = relationship(
        'Post',
        foreign_keys=[post_id],
        back_populates='photos'
    )

    def to_dict(self, req_post: bool = False) -> dict[str, object]:
        ret: dict[str, object] = {
            'id': str(self.id),
            'post_position': self.post_position,
            'image_src': self.image_src,
            'image_id': self.image_id
        }

        if req_post:
            ret['post'] = self.post.to_dict()
        
        return ret