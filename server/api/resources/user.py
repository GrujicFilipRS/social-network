from fastapi.responses import JSONResponse
from pydantic import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

from server.db.models.users import User
from server.db.db_session import create_session

from server.utils import jwt_tokens

from server.api.index import app

class UserRegister(BaseModel):
    username: str
    password: str


@app.get('/api/get_user/')
async def get_user(user_id: int | None, req_name: bool=False, req_creation_date=False):
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


@app.post('/api/register_user/')
async def register(user: UserRegister):
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


@app.post('/api/login/')
async def login(user: UserRegister):
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