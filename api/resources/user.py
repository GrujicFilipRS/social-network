from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

from server.db.models.users import User
from server.db.db_session import create_session

from server.utils import jwt_tokens

from index import app

class UserRegister(BaseModel):
    username: str
    password: str


class NameSetter(BaseModel):
    new_name: str


class UsernameSetter(BaseModel):
    username: str


class AuthorizationHeader(BaseModel):
    Authorization: str


@app.get('user/get_user/')
async def get_user(user_id: int | None, req_name: bool=False, req_creation_date=False) -> JSONResponse:
    db_session = create_session()

    if user_id is None:
        return JSONResponse(content={'message': '`user_id` parameter is necessary'}, status_code=400)

    try:
        user = db_session.get(User, user_id)

        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)
        
        content: dict = {
            'message': 'User found',
            'user': user.to_dict(req_name=req_name, req_creation_date=req_creation_date)
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'An error occured: {str(e)}'}, status_code=500)
    
    finally:
        db_session.close()


@app.post('/user/register/')
async def register(user: UserRegister) -> JSONResponse:
    username = user.username
    password = user.password

    if not username or not password:
        return JSONResponse(content={'message': 'Username and password required'}, status_code=400)
    
    db_sess = create_session()

    try:
        if db_sess.query(User).filter_by(username=username).first():
            return JSONResponse(content={'message': 'User with such username already exists'}, status_code=400)
        
        user = User(username=username)
        user.set_password(password)
        user.set_creation_date(datetime.now())

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


@app.post('/user/login/')
async def login(user: UserRegister) -> JSONResponse:
    username = user.username
    password = user.password

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
            'token': token
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while logging in: {e}'}, status_code=500)

    finally:
        db_sess.close()


@app.put('/user/set_name/')
async def set_user_name(body: NameSetter, headers: Annotated[AuthorizationHeader, Header()]) -> JSONResponse:
    new_name: str = body.new_name
    token: str = headers.Authorization

    if not new_name or not token:
        return JSONResponse(content={'message': 'New name and token required'}, status_code=400)

    user_id: int = jwt_tokens.get_user_from_token(token)

    if user_id == -1:
        return JSONResponse(content={'message': 'Invalid authorization'}, status_code=400)
    
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


@app.put('/user/change_username/')
async def change_username(body: UsernameSetter, headers: Annotated[AuthorizationHeader, Header()]) -> JSONResponse:
    new_username: str = body.username
    token: str = headers.Authorization

    if not new_username or not token:
        return JSONResponse(content={'message': 'New username and token required'}, status_code=400)
    
    user_id: int = jwt_tokens.get_user_from_token(token)

    if user_id == -1:
        return JSONResponse(content={'message': 'Invalid authorization'}, status_code=400)

    db_sess = create_session()

    try:
        user: User | None = db_sess.query(User).filter_by(id=user_id).first()

        if user.username == new_username: # Didn't actually change the username
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