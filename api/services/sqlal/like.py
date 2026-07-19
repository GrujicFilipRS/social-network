from sqlalchemy.orm import Session

from ..service_models import LikeServiceModel


class LikeServiceSqlal(LikeServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
