from functools import wraps
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID
import inspect

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
    is_async = inspect.iscoroutinefunction(func)

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        request = kwargs.get('request') or next(
            (arg for arg in args if isinstance(arg, Request)),
            None,
        )

        if request is None:
            raise RuntimeError(
                '@require_auth requires `request: Request` parameter'
            )

        token = request.headers.get('Authorization')
        if not token:
            raise JSONResponse(
                status_code=401,
                detail='Missing Authorization header',
            )

        user_id = decode_token(token)
        if not user_id:
            raise JSONResponse(
                status_code=401,
                detail='Invalid or expired token',
            )

        kwargs["user_id"] = user_id

        if is_async:
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return async_wrapper