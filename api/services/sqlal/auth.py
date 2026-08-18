from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from env import Env
from models import User
from sqlalchemy.orm import Session

from ..service_models import AuthServiceModel


class AuthServiceJWTSqlal(AuthServiceModel):
    def __init__(self, db_sess: Session):
        self.db_session = db_sess
        super().__init__()
    
    def encode_token(self, user_id: UUID | str) -> str:
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(hours=Env.JWT_EXPIRATION_HOURS)
        payload = {
            'user_id': str(user_id),
            'iat': int(now.timestamp()),
            'exp': int(expiration.timestamp()),
        }
        token = jwt.encode(payload, Env.SECRET_KEY, algorithm='HS256')
        return token
    
    def decode_token(self, token: str | None) -> UUID | None:
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, Env.SECRET_KEY, algorithms=['HS256'])
            return UUID(payload.get('user_id'))
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_from_token(self, token: str) -> User | None:
        user_id = self.decode_token(token)
        
        if not user_id:
            return None
        
        user = self.db_session.get(User, user_id)
        
        return user