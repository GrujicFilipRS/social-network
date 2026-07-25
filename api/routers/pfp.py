from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from fastapi.datastructures import UploadFile
from fastapi.responses import JSONResponse
from models import PFP
from schemas import DTO
from services.service_models import PfpServiceModel
from utils import JWT

router = APIRouter()


@router.post(
    '/create_user_pfp/',
    response_model=DTO
)
@inject
async def create_user_pfp(
    request: Request,
    pfp_service: FromDishka[PfpServiceModel]
) -> JSONResponse:
    user_id = JWT.get_id_from_request(request)
    
    if not user_id:
        return DTO.error('Unauthorized')
    
    form = await request.form()
    form_image = form.get('image')

    if not await PFP.approve_pfp_file(form_image):
        return DTO.error('Invalid image file')
        
    if not isinstance(form_image, UploadFile):
        return DTO.error('Image file is required')
    
    response = await pfp_service.create_pfp(user_id, form_image.file)
    
    return response
