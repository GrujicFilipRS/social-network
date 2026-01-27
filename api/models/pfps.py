from sqlalchemy import Column, ForeignKey, UUID, String
from sqlalchemy.orm import relationship
from db.db_session import SqlAlchemyBase
from uuid import uuid4

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