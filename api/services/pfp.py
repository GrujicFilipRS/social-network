from uuid import UUID
from fastapi import Request
from fastapi.responses import JSONResponse

import cloudinary
import cloudinary.uploader
import io

from fastapi import APIRouter

from env import Env
from models.pfps import PFP
from db.db_session import DBSessionManager

from utils.jwt_tokens import require_auth

router = APIRouter()

cloudinary.config(
    cloud_name=Env.CLOUDINARY_CLOUD_NAME,
    api_key=Env.CLOUDINARY_API_KEY,
    api_secret=Env.CLOUDINARY_API_SECRET,
    secure=True
)


@router.get('/get_user_pfp/')
def get_user_pfp(user_id: str | UUID) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            user_uuid: UUID = UUID(str(user_id))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid user_id'}, status_code=400)

        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_uuid).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)
        
        content: dict = {
            'message': 'Successfully found pfp',
            'image_src': pfp.image_src
        }

        return JSONResponse(content=content, status_code=200)

@router.post('/create_user_pfp/')
@require_auth
async def create_user_pfp(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        form = await request.form()
        image = form.get('image')

        if not PFP.approve_pfp_file(image):
            return JSONResponse(content={'message': 'Invalid image file'}, status_code=400)

        file_bytes = await image.read()

        result = cloudinary.uploader.upload(
            io.BytesIO(file_bytes),
            folder=Env.CLOUDINARY_PFP_FOLDER,
            resource_type='image',
            public_id=image.filename.split('.')[0],
            overwrite=True
        )

        image_src: str = result['secure_url']
        image_id: str = result['public_id']

        previous_pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if not previous_pfp is None:
            cloudinary.uploader.destroy(previous_pfp.image_id)
            db_sess.delete(previous_pfp)
            db_sess.commit()
        
        new_pfp = PFP(user_id=user_id, image_src=image_src, image_id=image_id)
        db_sess.add(new_pfp)
        db_sess.commit()

        content: dict = {
            'message': 'PFP successfully created',
            'image_src': image_src
        }

        return JSONResponse(content=content, status_code=201)

@router.delete('/delete_pfp/')
@require_auth
async def delete_pfp(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)

        cloudinary.uploader.destroy(pfp.image_id)

        db_sess.delete(pfp)
        db_sess.commit()

        return JSONResponse(content={'message': 'pfp successfully deleted'}, status_code=200)