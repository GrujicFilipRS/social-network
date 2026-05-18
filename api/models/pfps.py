from __future__ import annotations

from typing import TYPE_CHECKING, Any
import uuid
from fastapi import UploadFile
from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db import SqlAlchemyBase
from uuid import uuid4
from PIL import Image
from io import BytesIO

if TYPE_CHECKING:
    from models import User

class PFP(SqlAlchemyBase):
    __tablename__ = 'pfps'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
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

    user: Mapped['User'] = relationship(
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

    @staticmethod
    async def approve_pfp_file(pfp: Any) -> bool:
        MAX_SIZE = 5 * 1024 * 1024  # 5MB
        ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}

        if pfp is None or not isinstance(pfp, UploadFile):
            return False

        if not pfp.content_type or not pfp.content_type.startswith('image/'):
            return False

        try:
            file_bytes = await pfp.read()
        except Exception:
            return False

        if len(file_bytes) == 0 or len(file_bytes) > MAX_SIZE:
            return False

        try:
            img = Image.open(BytesIO(file_bytes))
            img.verify()
        except Exception:
            return False

        if img.format not in ALLOWED_FORMATS:
            return False

        try:
            img = Image.open(BytesIO(file_bytes))
            w, h = img.size
            if w > 2048 or h > 2048:
                return False
        except Exception:
            return False

        return True
