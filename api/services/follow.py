from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated

from ..server.db.models.follows import Follow
from ..server.db.models.users import User
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

from fastapi import APIRouter

router = APIRouter()


class ToFollowData(BaseModel):
    to_follow_id: int


@router.get('/get_follow/')
def get_follow(follow_id: int, req_names: bool = False) -> JSONResponse:
    try:
        db_sess = create_session()

        follow: Follow | None = db_sess.get(Follow, follow_id)

        if follow is None:
            return JSONResponse(content={'message': 'Follow not found'}, status_code=404)
        
        content: dict = {
            'message': 'Follow successfully found',
            'follow': follow.to_dict(req_names=req_names)
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting follow: {e}'}, status_code=400)

    finally:
        db_sess.close()


@router.post('/follow_user/')
def follow_user(
    data: ToFollowData,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    try:
        token: str = headers.Authorization

        if not token:
            return JSONResponse(content={'message': 'Invalid authorization'}, status_code=401)

        user_id: int = jwt_tokens.get_user_from_token(token)

        if user_id == -1:
            return JSONResponse(content={'message': 'Invalid authorization'}, status_code=401)

        db_sess = create_session()

        if not db_sess.get(User, data.to_follow_id):
            return JSONResponse(content={'message': 'User not found'}, status_code=404)

        if db_sess.query(Follow).filter_by(follower_id=user_id, followed_id=data.to_follow_id).first():
            return JSONResponse(content={'message', 'You already follow this user'}, status_code=400)

        follow = Follow()
        follow.followed_id = data.to_follow_id
        follow.follower_id = user_id
        follow.followed_datetime = datetime.now(timezone.utc)

        db_sess.add(follow)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully followed user'}, status_code=201)
        
    except Exception as e:
        return JSONResponse(content={'message': f'Error while following: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.delete('/unfollow_user/')
def unfollow_user(
    data: ToFollowData,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    try:
        token: str = headers.Authorization

        if not token:
            return JSONResponse(content={'message': 'Invalid authorization'}, status_code=401)

        user_id: int = jwt_tokens.get_user_from_token(token)

        if user_id == -1:
            return JSONResponse(content={'message': 'Invalid authorization'}, status_code=401)

        db_sess = create_session()

        follow = db_sess.query(Follow).filter_by(
            follower_id=user_id,
            followed_id=data.to_follow_id
        ).first()

        db_sess.delete(follow)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully unfollowed user'}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message', f'Unexpected error while unfollowing user: {e}'})


@router.get('/get_user_follows/')
def get_user_follows( # Gets all of the people a user is following
    user_id: int
) -> JSONResponse:
    try:
        db_sess = create_session()

        if not db_sess.get(User, user_id):
            return JSONResponse(content={'message': 'User with provided id not found'}, status_code=404)

        follows = db_sess.query(Follow).filter_by(follower_id=user_id)

        follows_hashed: list[User] = []
        for follow in follows:
            user_followed = db_sess.get(User, follow.followed_id)
            if user_followed:
                follows_hashed.append({ 'id': user_followed.id, 'username': user_followed.username })
        
        content: dict = {
            'message': 'Successfully found followed users',
            'users': follows_hashed
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Unexpected error while getting user\'s follows: {e}'}, status_code=400)

    finally:
        db_sess.close()


@router.get('/get_user_followers/')
def get_user_followers(
    user_id: int
) -> JSONResponse:
    try:
        db_sess = create_session()

        if not db_sess.get(User, user_id):
            return JSONResponse(content={'message': 'User with provided id not found'}, status_code=404)

        follows = db_sess.query(Follow).filter_by(followed_id=user_id)

        follows_hashed: list[User] = []
        for follow in follows:
            user_followed = db_sess.get(User, follow.follower_id)
            if user_followed:
                follows_hashed.append({ 'id': user_followed.id, 'username': user_followed.username })
        
        content: dict = {
            'message': 'Successfully found followers',
            'users': follows_hashed
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Unexpected error while getting user\'s followers: {e}'}, status_code=400)

    finally:
        db_sess.close()