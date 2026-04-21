from typing import Any
from fastapi import UploadFile
from sqlalchemy import Column, ForeignKey, UUID, String
from sqlalchemy.orm import relationship
from db import SqlAlchemyBase
from uuid import uuid4
from PIL import Image
from io import BytesIO

class PFP(SqlAlchemyBase):
    __tablename__ = 'pfps'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    image_src = Column(String, nullable=False)
    image_id = Column(String, nullable=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='pfp')

    def to_dict(self, req_user: bool = False) -> dict:
        content: dict = {
            'id': str(self.id),
            'image_src': self.image_src,
            'image_id': self.image_id
        }

        if req_user:
            content['user'] = self.user.to_dict()
    
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
