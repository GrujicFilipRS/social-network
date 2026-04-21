from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime, timezone

from models import Follow, User
from db import DBSessionManager

from utils import JWT

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_follow/')
def get_follow(follow_id: int, req_names: bool = False) -> JSONResponse:
    with DBSessionManager() as db_sess:
        follow: Follow | None = db_sess.get(Follow, follow_id)

        if follow is None:
            return JSONResponse(content={'message': 'Follow not found'}, status_code=404)
        
        content: dict = {
            'message': 'Follow successfully found',
            'follow': follow.to_dict(req_names=req_names)
        }

        return JSONResponse(content=content, status_code=200)


@router.post('/follow_user/')
@JWT.require_auth
async def follow_user(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        to_follow_id: UUID = UUID((await request.json()).get('to_follow_id'))
        if to_follow_id == user_id:
            return JSONResponse(content={'message': 'You cannot follow yourself'}, status_code=400)

        if not db_sess.get(User, to_follow_id):
            return JSONResponse(content={'message': 'User not found'}, status_code=404)

        if db_sess.query(Follow).filter_by(follower_id=user_id, followed_id=to_follow_id).first():
            return JSONResponse(content={'message', 'You already follow this user'}, status_code=400)

        follow = Follow()
        follow.followed_id = to_follow_id
        follow.follower_id = user_id
        follow.followed_datetime = datetime.now(timezone.utc)

        db_sess.add(follow)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully followed user'}, status_code=201)


@router.delete('/unfollow_user/')
@JWT.require_auth
async def unfollow_user(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        to_unfollow_id: UUID = UUID((await request.json()).get('to_unfollow_id'))

        follow: Follow | None = db_sess.query(Follow).filter_by(
            follower_id=user_id,
            followed_id=to_unfollow_id
        ).first()

        if follow is None:
            return JSONResponse(content={'message': 'Follow relationship not found'}, status_code=404)

        db_sess.delete(follow)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully unfollowed user'}, status_code=200)


@router.get('/get_user_follows/')
def get_user_follows(
    user_id: str | UUID
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            user_id: UUID = UUID(user_id)
        except ValueError:
            return JSONResponse(content={'message': 'Invalid user id format'}, status_code=400)

        if not db_sess.get(User, user_id):
            return JSONResponse(content={'message': 'User with provided id not found'}, status_code=404)

        follows = db_sess.query(Follow).filter_by(follower_id=user_id)

        follows_hashed: list[User] = []
        for follow in follows:
            user_followed = db_sess.get(User, follow.followed_id)
            if user_followed:
                follows_hashed.append(user_followed.to_dict())
        
        content: dict = {
            'message': 'Successfully found followed users',
            'users': follows_hashed
        }

        return JSONResponse(content=content, status_code=200)


@router.get('/get_user_followers/')
def get_user_followers(
    user_id: str | UUID
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            user_id: UUID = UUID(user_id)
        except ValueError:
            return JSONResponse(content={'message': 'Invalid user id format'}, status_code=400)

        if not db_sess.get(User, user_id):
            return JSONResponse(content={'message': 'User with provided id not found'}, status_code=404)

        follows = db_sess.query(Follow).filter_by(followed_id=user_id)

        follows_hashed: list[User] = []
        for follow in follows:
            user_followed = db_sess.get(User, follow.follower_id)
            if user_followed:
                follows_hashed.append(user_followed.to_dict())
            
        content: dict = {
            'message': 'Successfully found followers',
            'users': follows_hashed
        }

        return JSONResponse(content=content, status_code=200)


@router.get('/check_if_following/')
def check_if_following(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            user_to_id: UUID = UUID(request.query_params.get('user_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid user id format'}, status_code=400)
        is_following: bool = bool(db_sess.query(Follow).filter_by(
            follower_id=user_id,
            followed_id=user_to_id
        ).first())

        return JSONResponse(content={'following': is_following}, status_code=200)