from io import BytesIO
from typing import Annotated
from uuid import UUID
from starlette.datastructures import UploadFile
from fastapi.responses import JSONResponse
from fastapi import Depends, File, Form, Request
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from models import Post, Like
from db import DBSessionManager
from services.service_models import PostServiceModel

from utils import JWT, PostLiterals

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_post/')
@inject
@JWT.optional_auth
async def get_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        post_id: UUID | None = UUID(request.query_params.get('post_id'))
    except ValueError:
        return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

    with DBSessionManager() as db_sess:
        post = db_sess.get(Post, post_id)
        
        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        post_info: dict = post.to_dict(
            req_likes = True,
            req_comments = True
        )

        content: dict = {
            'message': 'Post found',
            'post': post_info
        }
        
        content['post']['liked_by_user'] = db_sess.query(Like).filter(
            Like.post_id == post_id,
            Like.user_id == user_id
        ).first() is not None
        
        if post.status == PostLiterals.PRIVATE and user_id != post.user_id:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        return JSONResponse(content=content, status_code=200)


@router.get('/get_post_id_from_like_id/{like_id}')
@JWT.optional_auth
async def get_post_id_from_like_id(
    request: Request,
    like_id: UUID,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        like = db_sess.query(Like).get(like_id)

        if not like:
            return JSONResponse(content={'message': 'Like not found'}, status_code=404)

        post = db_sess.get(Post, like.post_id)

        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        if post.status == PostLiterals.PRIVATE and user_id != post.user_id:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        return JSONResponse(content={'post_id': str(post.id)}, status_code=200)


@router.post('/create_post/')
@inject
async def create_post(
    title: Annotated[str, Form()],
    body: Annotated[str | None, Form()],
    status: Annotated[str, Form()],
    images: Annotated[list[UploadFile], File()] = [],
    post_service: FromDishka[PostServiceModel] = Depends(),
    user_id: UUID | None = None,
):
    image_streams = [
        BytesIO(await image.read())
        for image in images
    ]

    return await post_service.create_post(
        user_id=user_id,
        title=title,
        body=body,
        status=status,
        image_streams=image_streams,
    )


@router.put('/edit_post/')
@JWT.require_auth
async def edit_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None

    with DBSessionManager() as db_sess:
        data = await request.json()

        if not Post.verify_edit(data):
            return JSONResponse(content={'message': 'Invalid creation data'}, status_code=400)

        title: str = data.get('title').strip()
        body: str = data.get('body').strip()
        status: str = data.get('status').strip().upper()

        try:
            post_id: UUID = UUID(data.get('id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post id'}, status_code=400)
        
        post = db_sess.get(Post, post_id)

        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        post.set_title(title)
        post.set_body(body)
        post.set_status(status)

        db_sess.add(post)
        db_sess.commit()

        content: dict = {
            'message': 'Successfully edited post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=200)


@router.delete('/delete_post/')
@JWT.require_auth
async def delete_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None

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
