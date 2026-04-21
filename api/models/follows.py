from sqlalchemy import Column, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from db import SqlAlchemyBase
from uuid import uuid4

class Follow(SqlAlchemyBase):
    __tablename__ = 'follows'

    id = Column(UUID, primary_key=True, default=uuid4)
    followed_datetime = Column(DateTime, nullable=False)
    follower_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    followed_id = Column(UUID, ForeignKey('users.id'), nullable=False)

    follower = relationship('User', foreign_keys=[follower_id], back_populates='follows')
    followed = relationship('User', foreign_keys=[followed_id], back_populates='followers')

    def to_dict(self, req_names=False) -> dict:
        data: dict = {
            'id': str(self.id),
            'followed_at': str(self.followed_datetime)
        }

        if req_names:
            data['follower'] = self.follower.to_dict()
            data['followed'] = self.followed.to_dict()
        else:
            data['follower_id'] = str(self.follower_id)
            data['followed_id'] = str(self.followed_id)
        
        return data