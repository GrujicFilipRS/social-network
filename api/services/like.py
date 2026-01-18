from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime, timezone

from server.db.models.likes import Like
from server.db.models.users import User
from server.db.models.posts import Post
from server.db.db_session import DBSessionManager

from server.utils.jwt_tokens import optional_auth, require_auth
from server.utils.literals import PostLiterals

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_like/')
@optional_auth
def get_like(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            like_id: UUID | None = UUID(request.query_params.get('like_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid like_id'}, status_code=400)

        like: Like | None = db_sess.get(Like, like_id)

        if not like:
            return JSONResponse(content={'message': 'Like not found'}, status_code=404)
        
        if (like.post.status == PostLiterals.PRIVATE and
            user_id != like.post.user_id):
            return JSONResponse(content={'message': 'The liked post is private'}, status_code=401)

        content: dict = {
            'message': 'Like successfully found',
            'like': like.to_dict()
        }

        return JSONResponse(content=content, status_code=200)


@router.post('/like_post/')
@require_auth
async def like_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            post_id: UUID = UUID(data.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        user: User | None = db_sess.get(User, user_id)
        if not user:
            return JSONResponse(content={'message': 'You must be logged in to like a message'}, status_code=401)

        if any([like.post_id == post_id for like in user.likes]):
            return JSONResponse(content={'message': 'You already liked this post'}, status_code=400)
        
        post: Post | None = db_sess.get(Post, post_id)
        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        like = Like()
        like.post_id = post_id
        like.user_id = user_id
        like.liked_at = datetime.now(timezone.utc)

        db_sess.add(like)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully liked post'}, status_code=201)
    

@router.delete('/unlike_post/')
@require_auth
async def unlike_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            post_id: UUID = UUID(data.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        user: User | None = db_sess.get(User, user_id)
        if not user:
            return JSONResponse(content={'message': 'You must be logged in to unlike a message'}, status_code=401)

        if not any([like.post_id == post_id for like in user.likes]):
            return JSONResponse(content={'message': 'The post isn\'t liked'}, status_code=400)

        like: Like | None = db_sess.query(Like).filter_by(user_id=user_id, post_id=post_id).first()

        if not like:
            return JSONResponse(content={'message': 'Like not found'}, status_code=404)
        
        db_sess.delete(like)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully unliked post'}, status_code=200)


@router.get('/get_user_likes/')
def get_user_likes(user_id: str) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            user_uuid: UUID = UUID(str(user_id))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid user_id'}, status_code=400)

        user: User | None = db_sess.get(User, user_uuid)

        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)
        
        content: dict = {
            'message': 'Likes successfully found',
            'likes': [ like.to_dict() for like in user.likes ]
        }

        return JSONResponse(content=content, status_code=200)