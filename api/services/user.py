from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime, timezone
from typing import Any

from server.db.models.users import User
from server.db.models.follows import Follow
from server.db.db_session import create_session

from server.utils import jwt_tokens
from server.utils.jwt_tokens import require_auth

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_user/')
async def get_user(
    user_id: int | None,
    req_name: bool = False,
    req_creation_date: bool = False,
    req_pfp: bool = False
) -> JSONResponse:
    db_session = create_session()

    if user_id is None:
        return JSONResponse(content={'message': '`user_id` parameter is necessary'}, status_code=400)

    try:
        user = db_session.get(User, user_id)

        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)
        
        content: dict = {
            'message': 'User found',
            'user': user.to_dict(req_name=req_name, req_creation_date=req_creation_date, req_pfp=req_pfp)
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'An error occured: {str(e)}'}, status_code=500)
    
    finally:
        db_session.close()


@router.get('/get_current_user/')
@require_auth
def get_current_user(
    request: Request,
    user_id: UUID | None = None,
) -> JSONResponse:
    try:
        db_sess = create_session()
        if not db_sess.get(User, user_id):
            return JSONResponse(content={'message': 'Invalid token'}, status_code=401)

        content: dict[str, str] = {
            'message': 'Successful verification',
            'user_id': str(user_id)
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while creating user: {e}'}, status_code=500)


@router.post('/register/')
async def register(request: Request) -> JSONResponse:
    data = await request.json()

    username: str | None = data.get('username')
    password: str | None = data.get('password')
    name: str | None = data.get('name')

    if not username or not password:
        return JSONResponse(content={'message': 'Username and password required'}, status_code=400)

    if not User.validate_username(username) or not User.validate_password(password):
        return JSONResponse(content={'message': 'Invalid username or password format'}, status_code=400)
    
    db_sess = create_session()

    try:
        if db_sess.query(User).filter_by(username=username).first():
            return JSONResponse(content={'message': 'User with such username already exists'}, status_code=400)
        
        user = User(username=username)
        user.set_password(password)
        user.set_creation_date(datetime.now(timezone.utc))
        if name:
            user.set_name(name)

        db_sess.add(user)
        db_sess.commit()
        
        token = jwt_tokens.encode_token(user.id)

        content: dict = {
            'message': 'User created and logged in',
            'user': user.to_dict(),
            'token': token
        }

        return JSONResponse(content=content, status_code=201)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while creating user: {e}'}, status_code=500)
    
    finally:
        db_sess.close()


@router.post('/login/')
async def login(request: Request) -> JSONResponse:
    data = await request.json()

    username: str | None = data.get('username')
    password: str | None = data.get('password')

    if not username or not password:
        return JSONResponse(content={'message': 'Username and password required'}, status_code=400)

    db_sess = create_session()

    try:
        if not db_sess.query(User).filter_by(username=username).first():
            return JSONResponse(content={'message': 'Incorrect credentials'}, status_code=400)
        
        user = db_sess.query(User).filter_by(username=username).first()

        if not user.check_password(password):
            return JSONResponse(content={'message': 'Incorrect credentials'}, status_code=400)
        
        token = jwt_tokens.encode_token(user.id)

        content: dict = {
            'message': 'User logged in',
            'user': user.to_dict(),
            'token': str(token)
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while logging in: {e}'}, status_code=500)

    finally:
        db_sess.close()


@router.put('/set_name/')
@require_auth
async def set_user_name(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    data: Any = await request.json()
    
    new_name: str | None = data.get('new_name')

    if not new_name:
        return JSONResponse(content={'message': 'New name required'}, status_code=400)
    
    db_sess = create_session()

    try:
        user: User | None = db_sess.query(User).filter_by(id=user_id).first()
        if User is None:
            return JSONResponse(content={'message': 'User doesn\'t exist'}, status_code=400)
        
        user.set_name(new_name)
        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': f'Name successfully changed to {new_name}'}, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while setting name: {e}'}, status_code=500)

    finally:
        db_sess.close()


@router.put('/change_username/')
@require_auth
async def change_username(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    data: Any = await request.json()

    new_username: str | None = data.get('new_username')
    if not new_username:
        return JSONResponse(content={'Invalid username format'}, status_code=400)

    if not User.validate_username(new_username):
        return JSONResponse(content={'Invalid username format'}, status_code=400)

    db_sess = create_session()

    try:
        user: User | None = db_sess.query(User).filter_by(id=user_id).first()

        if user.username == new_username:
            return JSONResponse(content={'message': 'That doesn\'t change the username'}, status_code=400)

        if db_sess.query(User).filter_by(username=new_username).first():
            return JSONResponse(content={'message': 'User with such username already exists'}, status_code=400)
        
        if user is None:
            return JSONResponse(content={'message': 'User doesn\'t exist'}, status_code=400)
        
        user.set_username(new_username)

        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': f'Username successfully changed to {new_username}'}, status_code=200)
        
    except Exception as e:
        return JSONResponse(content={'message': f'Error while changing username: {e}'}, status_code=500)
    
    finally:
        db_sess.close()


@router.put('/change_password/')
@require_auth
async def change_username(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    data: Any = await request.json()
    old_password: str | None = data.get('old_password')
    new_password: str | None = data.get('new_password')
    
    if not old_password or not new_password:
        return JSONResponse(content={'message': 'New password and old password required'}, status_code=400)
    
    if old_password == new_password:
        return JSONResponse(content={'message': 'New password must be different than old password'}, status_code=400)
    
    if not User.validate_password(new_password):
        return JSONResponse(content={'message': 'Invalid new password format'}, status_code=400)

    try:
        db_sess = create_session()

        user: User | None = db_sess.query(User).filter_by(id=user_id).first()

        if not user:
            return JSONResponse(content={'message': 'Not authenticated'}, status_code=401)

        if not user.check_password(old_password):
            return JSONResponse(content={'message': 'Invalid old password'}, status_code=401)
        
        user.set_password(new_password)

        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully changed password'}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while changing password: {e}'}, status_code=500)
    
    finally:
        db_sess.close()


@router.get('/get_user_profile/')
async def get_user_profile(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        data = await request.json()
        username: str | None = data.get('username')

        db_sess = create_session()
        
        user: User | None = db_sess.query(User).filter_by(username=username).first()
        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)

        user_followed: bool = not db_sess.query(Follow).filter_by(follower_id=user_id, followed_id=user.id).first() is None

        content: dict = {
            'message': 'User profile found',
            'user_id': str(user.id),
            'username': user.username,
            'user_name': user.name,
            'num_followers': len(user.followers),
            'num_followed': len(user.follows),
            'posts': [ post.to_dict() for post in user.posts ],
            'pfp_src': user.pfp.image_src if user.pfp else None,
            'user_followed': user_followed
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={'message': f'Error while getting user profile: {e}'},
            status_code=500
        )
    
    finally:
        db_sess.close()

@router.get('/get_current_user_profile/')
@require_auth
def get_current_user_profile(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        db_sess = create_session()

        user: User | None = db_sess.get(User, user_id)
        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)
        
        content: dict = {
            'message': 'User profile found',
            'user_id': str(user.id),
            'username': user.username,
            'user_name': user.name,
            'num_followers': len(user.followers),
            'num_followed': len(user.follows),
            'posts': [ post.to_dict() for post in user.posts ],
            'pfp_src': user.pfp.image_src if user.pfp else None
        }
        
        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={'message': f'Error while getting user profile: {e}'},
            status_code=500
        )
    
    finally:
        db_sess.close()