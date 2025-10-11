from fastapi import Header, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Annotated

import cloudinary
import cloudinary.uploader
import os, io

from fastapi import APIRouter

from ..server.db.models.pfps import PFP
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)


@router.get('/get_user_pfp/')
def get_user_pfp(user_id: int) -> JSONResponse:
    try:
        db_sess = create_session()
        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)
        
        content: dict = {
            'message': 'Successfully found pfp',
            'image_src': pfp.image_src
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting user pfp: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.post('/create_user_pfp/')
async def create_user_pfp(
    headers: Annotated[AuthorizationHeader, Header()],
    image: UploadFile = File(...)
) -> JSONResponse:
    
    try:
        db_sess = create_session()
        token: str = headers.Authorization
        user_id: int = jwt_tokens.get_user_from_token(token)

        if user_id == -1:
            return JSONResponse(content={'message': 'You are not authorized to do this'}, status_code=401)

        if not image.content_type.startswith('image/'):
            return JSONResponse(content={'message': 'File must be an image!'}, status_code=400)

        file_bytes = await image.read()

        result = cloudinary.uploader.upload(
            io.BytesIO(file_bytes),
            folder='fastapi_uploads_pfp',
            resource_type='image',
            public_id=image.filename.split(".")[0],
            overwrite=True
        )

        image_src: str = result['secure_url']

        previous_pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if not previous_pfp is None:
            db_sess.delete(previous_pfp)
            db_sess.commit()
        
        new_pfp = PFP()
        new_pfp.user_id = user_id
        new_pfp.image_src = image_src

        db_sess.add(new_pfp)
        db_sess.commit()

        content: dict = {
            'message': 'PFP successfully created',
            'image_src': image_src
        }

        return JSONResponse(content=content, status_code=201)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while creating user pfp: {e}'}, status_code=400)
    
    finally:
        db_sess.close()