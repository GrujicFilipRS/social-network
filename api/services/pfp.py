from uuid import UUID
from fastapi import Request, APIRouter
from fastapi.datastructures import UploadFile
from fastapi.responses import JSONResponse

from utils import ImageController, JWT
from models import PFP
from db import DBSessionManager

router = APIRouter()


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
@JWT.require_auth
async def create_user_pfp(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    form = await request.form()
    form_image = form.get('image')

    if not PFP.approve_pfp_file(form_image):
        return JSONResponse(content={'message': 'Invalid image file'}, status_code=400)
        
    if not isinstance(form_image, UploadFile):
        return JSONResponse(content={'message': 'Image file is required'}, status_code=400)
        
    image_src, image_id = await ImageController.create_image(form_image)
    
    with DBSessionManager() as db_sess:
        previous_pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if previous_pfp is not None:
            await ImageController.destroy_image(previous_pfp.image_id)
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
@JWT.require_auth
async def delete_pfp(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)

        await ImageController.destroy_image(pfp.image_id)

        db_sess.delete(pfp)
        db_sess.commit()

        return JSONResponse(content={'message': 'pfp successfully deleted'}, status_code=200)