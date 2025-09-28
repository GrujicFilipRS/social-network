from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime)

    posts = relationship('Post', back_populates='user')

    def to_dict(self, req_name=False, req_creation_date=False) -> dict:
        output: dict = {
            'id': self.id,
            'username': self.username,
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