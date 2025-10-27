from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase

class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False)
    post_position = Column(Integer, nullable=False)
    image_src = Column(String, nullable=False)
    image_id = Column(String, nullable=False)

    post = relationship('Post', foreign_keys=[post_id], back_populates='photos')

    def to_dict(self, req_post: bool = False) -> dict:
        ret: dict = {
            'id': self.id,
            'post_position': self.post_position,
            'image_src': self.image_src,
            'image_id': self.image_id
        }

        if req_post:
            ret['post'] = self.post.to_dict()
        else:
            ret['post_id'] = self.post_id
        
        return ret