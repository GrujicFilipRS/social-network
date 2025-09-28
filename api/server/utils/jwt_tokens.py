from functools import wraps
import jwt
from datetime import datetime, timezone, timedelta

from server.conf import Config

def encode_token(user_id: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    payload = {
        'user_id': user_id,
        'exp': expiration,
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        print("JWT Error: Signature has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"JWT Error: Invalid token. {e}")
        return None


def get_user_from_token(token: str) -> int:
    if not token:
        return -1
    
    user_id = decode_token(token)

    if not user_id:
        return -1
    
    return user_id