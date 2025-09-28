from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase

class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(Text)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts', overlaps='posts,users')

    def to_dict(self, req_creation_date=False) -> dict:
        output: dict = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'status': self.status,
            'user_id': self.user_id
        }

        if req_creation_date:
            output['created_at'] = str(self.created_at)
        
        return output

    def set_title(self, title: str) -> None:
        self.title = title
    
    def set_body(self, body: str) -> None:
        self.body = body
    
    def set_status(self, status: str) -> None:
        self.status = status