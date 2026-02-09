import re, regex
from sqlalchemy import Column, UUID, String, DateTime
from sqlalchemy.orm import relationship
from db.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime)
    last_username_edit = Column(DateTime)

    posts = relationship('Post', back_populates='user')
    
    follows = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower')
    followers = relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed')

    likes = relationship('Like', foreign_keys='Like.user_id', back_populates='user')

    comments = relationship('Comment', foreign_keys='Comment.creator_id', back_populates='creator')

    pfp = relationship('PFP', foreign_keys='PFP.user_id', back_populates='user', uselist=False)

    def to_dict(self, req_name=False, req_creation_date=False) -> dict:
        output: dict = {
            'id': str(self.id),
            'username': self.username,
            'pfp': self.pfp.image_src if self.pfp else ''
        }

        if req_name:
            output['name'] = self.name
        
        if req_creation_date:
            output['created_at'] = str(self.created_at)

        return output

    def set_password(self, password) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password) -> str:
        return check_password_hash(self.hashed_password, password)
    
    def set_creation_date(self, creation_date: DateTime) -> None:
        self.created_at = creation_date

    def set_name(self, name: str) -> None:
        self.name = name
    
    def set_username(self, username: str) -> None:
        self.username = username
    
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
        if name == '' or name is None: return True
        
        name_regex = regex.compile(r'^[\p{L}][\p{L}\p{M}\'\-.\s]*$')
        if not bool(name_regex.match(name)):
            return False

        return len(name) > 3 and len(name) < 30