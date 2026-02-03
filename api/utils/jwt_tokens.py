from functools import wraps
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID
from env import Env
import inspect

def encode_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(hours=Env.JWT_EXPIRATION_HOURS)
    payload = {
        'user_id': str(user_id),
        'iat': int(now.timestamp()),
        'exp': int(expiration.timestamp()),
    }
    token = jwt.encode(payload, Env.SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> UUID | None:
    try:
        payload = jwt.decode(token, Env.SECRET_KEY, algorithms=['HS256'])
        return UUID(payload.get('user_id'))
    except jwt.ExpiredSignatureError:
        print('JWT Error: Signature has expired.')
        return None
    except jwt.InvalidTokenError as e:
        print(f'JWT Error: Invalid token. {e}')
        return None


AUTH_COOKIE_NAME: str = 'access_token'

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

        token = request.cookies.get(AUTH_COOKIE_NAME)
        if not token:
            return JSONResponse(
                status_code=401,
                content={'message': 'Missing Authorization Cookie'}
            )

        user_id: UUID | None = decode_token(token)
        if not user_id:
            return JSONResponse(
                status_code=401,
                content={'message': 'Invalid or expired token'}
            )

        kwargs['user_id'] = user_id

        if is_async:
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return async_wrapper


def optional_auth(func):
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

        token = request.cookies.get(AUTH_COOKIE_NAME)

        user_id: UUID | None = decode_token(token) if token else None
        kwargs['user_id'] = user_id

        if is_async:
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return async_wrapper