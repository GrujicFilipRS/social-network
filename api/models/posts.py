from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING
import uuid
from uuid import uuid4
import unicodedata
from fastapi import UploadFile as FastAPIUploadFile
from starlette.datastructures import UploadFile
from fastapi.datastructures import FormData
from sqlalchemy import DateTime, ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db import SqlAlchemyBase

if TYPE_CHECKING:
    from models import Comment, Like, Photo, User


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
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

    user: Mapped['User'] = relationship(
        'User',
        back_populates='posts'
    )
    likes: Mapped[list['Like']] = relationship(
        'Like',
        back_populates='post',
        cascade='all, delete-orphan'
    )
    comments: Mapped[list['Comment']] = relationship(
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan'
    )
    photos: Mapped[list['Photo']] = relationship(
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

    @staticmethod
    async def verify_creation(data: FormData) -> bool:
        title: Any = data.get('title')
        body: Any = data.get('body')
        status: Any = data.get('status')

        if not isinstance(title, str) or not isinstance(body, str) or not isinstance(status, str):
            return False
        
        title: str = title.strip()
        body: str = body.strip()
        status: str = status.strip().upper()
        
        MIN_TITLE_LENGTH, MAX_TITLE_LENGTH = 3, 45
        if len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
            return False
        
        MAX_BODY_LENGTH = 280
        if len(body) > MAX_BODY_LENGTH:
            return False
        
        from utils import PostLiterals
        
        if status not in PostLiterals.LIST_LITS:
            return False
        
        if (not all(c.isprintable() or c in '\n\r\t' for c in title) or
            not all(c.isprintable() or c in '\n\r\t' for c in body)):
            return False
        
        MAX_BODY_LINES = 10
        if body.count('\n') > MAX_BODY_LINES:
            return False
        
        DANGEROUS_SUBSTRINGS = (
            '<script',
            '</script',
            'javascript:',
            'onerror=',
            'onload=',
        )

        lower_body = body.lower()
        if any(x in lower_body for x in DANGEROUS_SUBSTRINGS):
            return False
        
        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in body + title
        ):
            return False

        images = data.getlist('images') or []
        MAX_IMAGES = 10
        
        if len(images) > MAX_IMAGES:
            return False
        
        from models import Photo
        
        for image in images:
            if not isinstance(image, (UploadFile, FastAPIUploadFile)):
                return False
            
            if not await Photo.verify_valid_photo(image):
                return False
            
            # Reset image byte pointer
            await image.seek(0)
        
        return True
    
    @staticmethod
    def verify_edit(data: Any) -> bool:
        title: Any = data.get('title')
        body: Any = data.get('body')
        status: Any = data.get('status')

        if not isinstance(title, str) or not isinstance(body, str) or not isinstance(status, str):
            return False
        
        title: str = title.strip()
        body: str = body.strip()
        status: str = status.strip().upper()
        
        MIN_TITLE_LENGTH, MAX_TITLE_LENGTH = 3, 45
        if len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
            return False
        
        MAX_BODY_LENGTH = 280
        if len(body) > MAX_BODY_LENGTH:
            return False
        
        from utils import PostLiterals
        
        if status not in PostLiterals.LIST_LITS:
            return False
        
        if (not all(c.isprintable() or c in '\n\r\t' for c in title) or
            not all(c.isprintable() or c in '\n\r\t' for c in body)):
            return False
        
        MAX_BODY_LINES = 10
        if body.count('\n') > MAX_BODY_LINES:
            return False
        
        DANGEROUS_SUBSTRINGS = (
            '<script',
            '</script',
            'javascript:',
            'onerror=',
            'onload=',
        )

        lower_body = body.lower()
        if any(x in lower_body for x in DANGEROUS_SUBSTRINGS):
            return False
        
        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in body + title
        ):
            return False
        
        return True