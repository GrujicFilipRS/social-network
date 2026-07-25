from models import PFP, User
from schemas import DTO
from sqlalchemy.orm import Session
from utils import PhotoVerificationMethods

from ..service_models import ImageUploadServiceModel, PfpServiceModel


class PfpServiceSqlal(PfpServiceModel):
    def __init__(
        self,
        db_session: Session,
        upload_service: ImageUploadServiceModel
    ):
        self.db_session = db_session
        self.upload_service = upload_service
    
    async def create_pfp(self, user_id, image_stream) -> DTO:
        if not PhotoVerificationMethods.verify_pfp(image_stream):
            return DTO.error('Invalid image format')
        
        user_exists = self.db_session.get(User, user_id) is not None
        
        if not user_exists:
            return DTO.error('User doesn\'t exist')
        
        user_pfp = self.db_session.query(PFP).filter_by(user_id=user_id).first()
        if not user_pfp:
            user_pfp = PFP()
        
        image_src, public_id = await self.upload_service.create_image(image_stream)
        
        user_pfp.image_src = image_src
        user_pfp.public_id = public_id
        
        self.db_session.add(user_pfp)
        self.db_session.commit()
        
        return DTO.ok()