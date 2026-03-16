from fastapi import UploadFile
from sqlalchemy import Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from db.db_session import SqlAlchemyBase
from uuid import uuid4
from PIL import Image
from io import BytesIO

class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = Column(UUID, primary_key=True, default=uuid4)
    post_id = Column(UUID, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post_position = Column(Integer, nullable=False)
    image_src = Column(String, nullable=False)
    image_id = Column(String, nullable=False)

    post = relationship('Post', foreign_keys=[post_id], back_populates='photos')

    def to_dict(self, req_post: bool = False) -> dict:
        ret: dict = {
            'id': str(self.id),
            'post_position': self.post_position,
            'image_src': self.image_src,
            'image_id': self.image_id
        }

        if req_post:
            ret['post'] = self.post.to_dict()
        
        return ret

    @staticmethod
    async def verify_valid_photo(image: UploadFile) -> bool:
        MAX_SIZE = 15 * 1024 * 1024  # 15MB
        ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP', 'JPG'}

        if not image.content_type or not image.content_type.startswith('image/'):
            return False

        try:
            file_bytes = await image.read()
            await image.seek(0)
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

        img = Image.open(BytesIO(file_bytes))
        w, h = img.size
        if w > 6000 or h > 6000:
            return False
        
        if w < 300 or h < 300:
            return False

        return True
