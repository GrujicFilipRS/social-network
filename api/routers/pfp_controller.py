from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from fastapi.datastructures import UploadFile
from schemas import DTO
from services.service_models import AuthServiceModel, PfpServiceModel

router = APIRouter()


@router.post(
    '/create_user_pfp/',
    response_model=DTO
)
@inject
async def create_user_pfp(
    request: Request,
    auth_service: FromDishka[AuthServiceModel],
    pfp_service: FromDishka[PfpServiceModel]
):
    user = auth_service.get_user_from_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user:
        return DTO.error('Unauthorized')
    
    form = await request.form()
    form_image = form.get('image')
        
    if not isinstance(form_image, UploadFile):
        return DTO.error('Image file is required')
    
    response = await pfp_service.create_pfp(user.id, form_image.file)
    
    return response
