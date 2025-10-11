from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase

class PFP(SqlAlchemyBase):
    __tablename__ = 'pfps'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    image_src = Column(Text, nullable=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='pfp')

    def to_dict(self, req_user: bool = False) -> dict:
        content: dict = {
            'id': self.id,
            'image_src': self.image_src
        }

        if req_user:
            content['user'] = self.user.to_dict()