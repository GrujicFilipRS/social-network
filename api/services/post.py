from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import Request, UploadFile
from datetime import datetime, timezone

from models.posts import Post
from models.photos import Photo
from db.db_session import DBSessionManager

from utils.jwt_tokens import optional_auth, require_auth
from utils.literals import PostLiterals

from fastapi import APIRouter

from utils.image_controller import ImageController

router = APIRouter()


@router.get('/get_post/')
@optional_auth
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
    data = await request.form()

    if not await Post.verify_creation(data):
        return JSONResponse(content={'message': 'Invalid creation data'}, status_code=400)

    title: str = data.get('title').strip()
    body: str = data.get('body').strip()
    status: str = data.get('status').strip().upper()
    photos: list[UploadFile] = data.getlist('images')

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
        data = await request.form()

        if not Post.verify_creation(data):
            return JSONResponse(content={'message': 'Invalid creation data'}, status_code=400)

        title: str = data.get('title').strip()
        body: str = data.get('body').strip()
        status: str = data.get('status').strip().upper()
        photos: list[UploadFile] = data.getlist('images')

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
        db_sess.flush()
        
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