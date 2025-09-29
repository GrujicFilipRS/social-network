from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase

class Follow(SqlAlchemyBase):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True)
    followed_datetime = Column(DateTime, nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    follower = relationship('User', foreign_keys=[follower_id], back_populates='follows')
    followed = relationship('User', foreign_keys=[followed_id], back_populates='followers')

    def to_dict(self, req_names=False) -> dict:
        data: dict = {
            'id': self.id,
            'followed_at': str(self.followed_datetime)
        }

        if req_names:
            data['follower'] = self.follower.to_dict()
            data['followed'] = self.followed.to_dict()
        else:
            data['follower_id'] = self.follower_id
            data['followed_id'] = self.followed_id
        
        return data