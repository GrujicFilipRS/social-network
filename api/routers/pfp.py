from uuid import UUID
from dishka import FromDishka
from fastapi import Request, APIRouter
from fastapi.datastructures import UploadFile
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import inject

from services.service_models import ImageUploadServiceModel, UserServiceModel, PfpServiceModel
from utils import JWT
from models import PFP
from db import DBSessionManager
from schemas import DTO

router = APIRouter()


@router.post(
    '/create_user_pfp/',
    response_model=DTO
)
@inject
async def create_user_pfp(
    request: Request,
    user_service: FromDishka[UserServiceModel],
    pfp_service: FromDishka[PfpServiceModel],
    image_service: FromDishka[ImageUploadServiceModel]
) -> JSONResponse:
    user_id = JWT.get_id_from_request(request)
    form = await request.form()
    form_image = form.get('image')

    if not PFP.approve_pfp_file(form_image):
        return JSONResponse(content={'message': 'Invalid image file'}, status_code=400)
        
    if not isinstance(form_image, UploadFile):
        return JSONResponse(content={'message': 'Image file is required'}, status_code=400)
        
    image_src, image_id = await image_service.create_image(form_image)
    
    with DBSessionManager() as db_sess:
        previous_pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if previous_pfp is not None:
            await image_service.destroy_image(previous_pfp.image_id)
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
@inject
@JWT.require_auth
async def delete_pfp(
    request: Request,
    image_service: FromDishka[ImageUploadServiceModel],
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None

    with DBSessionManager() as db_sess:
        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)

        await image_service.destroy_image(pfp.image_id)

        db_sess.delete(pfp)
        db_sess.commit()

        return JSONResponse(content={'message': 'pfp successfully deleted'}, status_code=200)