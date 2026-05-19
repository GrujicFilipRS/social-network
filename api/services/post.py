from uuid import UUID
from starlette.datastructures import UploadFile
from fastapi.responses import JSONResponse
from fastapi import Request, UploadFile as FastAPIUploadFile
from datetime import datetime, timezone

from utils import NotificationController
from models import Post, Like, Photo
from db import DBSessionManager

from utils import JWT, PostLiterals, ImageController

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_post/')
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
@JWT.require_auth
async def create_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None
    data = await request.form()

    if not await Post.verify_creation(data):
        return JSONResponse(content={'message': 'Invalid creation data'}, status_code=400)

    title = data.get('title')
    body = data.get('body')
    status = data.get('status')

    assert isinstance(title, str)
    assert isinstance(body, str)
    assert isinstance(status, str)

    title = title.strip()
    body = body.strip()
    status = status.strip().upper()

    photos: list[UploadFile] = [
        photo for photo in data.getlist('images') or []
        if isinstance(photo, (UploadFile, FastAPIUploadFile))
    ]

    with DBSessionManager() as db_sess:
        post = Post(
            title=title,
            body=body,
            status=status,
            created_at=datetime.now(timezone.utc),
            user_id=user_id
        )
        
        db_sess.add(post)
        db_sess.flush()
        
        # User automatically likes their own post
        user_like = Like(
            user_id=user_id,
            post_id=post.id
        )
        
        db_sess.add(user_like)
        
        # Create all individual photos
        for position, photo in enumerate(photos):
            image_src, public_id = await ImageController.create_image(photo)
            
            photo_obj = Photo(
                post_id=post.id,
                post_position=position,
                image_src=image_src,
                image_id=public_id
            )
            
            db_sess.add(photo_obj)
        
        db_sess.commit()
        
        for follower in post.user.followers:
            await NotificationController.create_notification(
                session=db_sess,
                receiver_id=follower.follower_id,
                sender_id=user_id,
                object_type='post',
                object_id=post.id
            )

        content: dict = {
            'message': 'Successfully created post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=201)


@router.put('/edit_post/')
@JWT.require_auth
async def edit_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
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
