from typing import BinaryIO

import cloudinary
import cloudinary.api

from env import Env

from uuid import UUID, uuid4

from ..service_models import ImageUploadServiceModel


class ImageServiceCloudinary(ImageUploadServiceModel):
    def __init__(self): ...
    
    async def setup(self) -> None:
        cloudinary.config(
            cloud_name=Env.CLOUDINARY_CLOUD_NAME,
            api_key=Env.CLOUDINARY_API_KEY,
            api_secret=Env.CLOUDINARY_API_SECRET,
            secure=True
        )
    
    async def test_connection(self) -> None:
        result = cloudinary.api.config()
        print('Cloudinary connection successful!')
        print(f'Cloud name: {result.get('cloud_name')}')
    
    async def create_image(
        self,
        stream: BinaryIO,
        filename: str = str(uuid4()),
    ) -> tuple[str, str]:

        result = cloudinary.uploader.upload(
            stream,
            folder=Env.CLOUDINARY_PFP_FOLDER,
            resource_type='image',
            public_id=str(uuid4()),
            overwrite=True,
            filename=filename,
        )

        return result['secure_url'], result['public_id']
    
    async def destroy_image(self, public_id: UUID) -> None:
        cloudinary.uploader.destroy(public_id)