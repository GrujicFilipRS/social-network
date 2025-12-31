from functools import wraps
from fastapi import HTTPException, Request
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID

from ..conf import Config

def encode_token(user_id: UUID) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    payload = {
        'user_id': str(user_id),
        'exp': expiration,
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> UUID | None:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return UUID(payload.get('user_id'))
    except jwt.ExpiredSignatureError:
        print("JWT Error: Signature has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"JWT Error: Invalid token. {e}")
        return None


def get_user_from_token(token: str) -> UUID:
    if not token:
        return ''
    
    user_id = decode_token(token)

    if not user_id:
        return ''
    
    return user_id

def require_auth(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        user_id = decode_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return await func(request, *args, user_id=user_id, **kwargs)

    return wrapper