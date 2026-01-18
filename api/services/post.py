from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime, timezone

from server.db.models.posts import Post
from server.db.db_session import DBSessionManager

from server.utils.jwt_tokens import optional_auth, require_auth

from server.utils.literals import PostLiterals

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_post/')
@optional_auth
async def get_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            post_id: UUID | None = UUID(request.query_params.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        post = db_sess.get(Post, post_id)
        
        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        post_info: dict = post.to_dict(
            req_creation_date=request.query_params.get('req_creation_date') is not None
        )

        content: dict = {
            'message': 'Post found',
            'post': post_info
        }

        if request.query_params.get('req_user'):
            content['user'] = post.user.to_dict(req_name=True)
        else:
            content['user'] = post.user.username

        if post.status == PostLiterals.PUBLIC:
            return JSONResponse(content=content, status_code=200)
        
        if user_id != post.user_id:
            return JSONResponse(content={'message': 'You are not authorized to view this post'}, status_code=401)

        return JSONResponse(content=content, status_code=200)


@router.post('/create_post/')
@require_auth
async def create_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()

        post = Post()
        post.set_title(data.get('title'))
        post.set_body(data.get('body'))
        post.set_status(data.get('status'))
        post.user_id = user_id
        post.created_at = datetime.now(timezone.utc)

        db_sess.add(post)
        db_sess.commit()

        content: dict = {
            'message': 'Successfully created post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=201)


@router.put('/edit_post/')
@require_auth
async def edit_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()

        try:
            post_id: UUID = UUID(data.get('id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post id'}, status_code=400)
        
        post = db_sess.get(Post, post_id)

        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        post.set_title(data.get('title'))
        post.set_body(data.get('body'))
        post.set_status(data.get('status'))

        db_sess.add(post)
        db_sess.commit()

        content: dict = {
            'message': 'Successfully edited post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=200)


@router.delete('/delete_post/')
@require_auth
async def delete_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            post_id: UUID | None = UUID(data.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        post = db_sess.get(Post, post_id)

        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to delete this post'}, status_code=401)
        
        db_sess.delete(post)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully deleted post'}, status_code=200)