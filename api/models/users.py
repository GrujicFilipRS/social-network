from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
import regex
import uuid
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import DateTime, String, UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db import SqlAlchemyBase
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

if TYPE_CHECKING:
    from models import Comment, Follow, Like, PFP, Post

class UserOptions:
    USERNAME_UPDATE_LIMIT_HOURS = 24

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    last_username_edit: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    posts: Mapped[list['Post']] = relationship(
        'Post',
        back_populates='user'
    )
    follows: Mapped[list['Follow']] = relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        back_populates='follower'
    )
    followers: Mapped[list['Follow']] = relationship(
        'Follow',
        foreign_keys='Follow.followed_id',
        back_populates='followed'
    )
    likes: Mapped[list['Like']] = relationship(
        'Like',
        foreign_keys='Like.user_id',
        back_populates='user'
    )
    comments: Mapped[list['Comment']] = relationship(
        'Comment',
        foreign_keys='Comment.creator_id',
        back_populates='creator'
    )
    pfp: Mapped['PFP | None'] = relationship(
        'PFP',
        foreign_keys='PFP.user_id',
        back_populates='user',
        uselist=False
    )

    def to_dict(self, req_name: bool = False, req_creation_date: bool = False) -> dict[str, object]:
        output: dict[str, object] = {
            'id': str(self.id),
            'username': self.username,
            'pfp': self.pfp.image_src if self.pfp else None
        }

        if req_name:
            output['name'] = self.name
        
        if req_creation_date:
            output['created_at'] = str(self.created_at)

        return output

    def set_password(self, password: str) -> None:
        password_hasher = PasswordHasher()
        hashed_pwd = password_hasher.hash(password)
        self.hashed_password = hashed_pwd

    def check_password(self, password: str) -> bool:
        password_hasher = PasswordHasher()
        try:
            password_hasher.verify(self.hashed_password, password)
        except VerifyMismatchError:
            return False
        
        return True
    
    def set_creation_date(self, creation_date: datetime) -> None:
        self.created_at = creation_date

    def set_name(self, name: str) -> None:
        self.name = name
    
    def able_to_change_username(self) -> bool:
        if self.last_username_edit is None:
            return True

        last_edit = self.last_username_edit.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - last_edit

        if delta < timedelta(hours = UserOptions.USERNAME_UPDATE_LIMIT_HOURS):
            return False

        return True
    
    @staticmethod
    def validate_username(username: str) -> bool:
        pattern = re.compile(r'[a-zA-Z0-9_]*')

        if not pattern.match(username):
            return False

        if len(username) < 7 or len(username) > 15:
            return False

        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        return len(password) > 7 and len(password) < 15

    @staticmethod
    def validate_name(name: str | None) -> bool:
        if name == '' or name is None:
            return True
        
        name_regex = regex.compile(r'^[\p{L}][\p{L}\p{M}\'\-.\s]*$')
        if not bool(name_regex.match(name)):
            return False

        return len(name) > 3 and len(name) < 30