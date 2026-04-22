from functools import wraps
from fastapi import Request, WebSocket
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID
from env import Env
import inspect


class JWT:
    @staticmethod
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


    @staticmethod
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

    @staticmethod
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

            token = request.cookies.get(JWT.AUTH_COOKIE_NAME)
            if not token:
                return JSONResponse(
                    status_code=401,
                    content={'message': 'Missing Authorization Cookie'}
                )

            user_id: UUID | None = JWT.decode_token(token)
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


    @staticmethod
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

            token = request.cookies.get(JWT.AUTH_COOKIE_NAME)

            user_id: UUID | None = JWT.decode_token(token) if token else None
            kwargs['user_id'] = user_id

            if is_async:
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return async_wrapper


    @staticmethod
    def set_response_cookie(response: JSONResponse, token: str):
        response.set_cookie(
            key=JWT.AUTH_COOKIE_NAME,
            value=token,
            httponly=True,
            samesite='Lax',
            path='/',
            secure=Env.FLASK_ENV == 'production',
            expires=Env.JWT_EXPIRATION_HOURS * 3600
        )
    
    @staticmethod
    def required_auth_websocket(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            websocket = kwargs.get('websocket')

            if not isinstance(websocket, WebSocket):
                raise RuntimeError(
                    '@required_auth_websocket requires `websocket` parameter to be of type WebSocket'
                )

            websocket.accept()

            token = JWT.get_cookie_from_websocket(websocket)
            if not token:
                await websocket.close(code=1008, reason='Missing Authorization Cookie')
                return

            user_id: UUID | None = JWT.decode_token(token)
            if not user_id:
                await websocket.close(code=1008, reason='Invalid or expired token')
                return

            kwargs['user_id'] = user_id

            return await func(*args, **kwargs)

        return async_wrapper
    
    @staticmethod
    def get_cookie_from_websocket(websocket: WebSocket) -> str | None:
        cookie_header = websocket.headers.get('cookie')
        if not cookie_header:
            return None

        cookies = dict(
            item.strip().split('=', 1)
            for item in cookie_header.split(';')
        )
        return cookies.get(JWT.AUTH_COOKIE_NAME)