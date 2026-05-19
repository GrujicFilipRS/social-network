import cloudinary
import cloudinary.api
import cloudinary.uploader
import io
from fastapi import UploadFile as FastAPIUploadFile
from starlette.datastructures import UploadFile
from uuid import uuid4

from env import Env

class ImageController:
    @staticmethod
    def setup_connection() -> None:
        cloudinary.config(
            cloud_name=Env.CLOUDINARY_CLOUD_NAME,
            api_key=Env.CLOUDINARY_API_KEY,
            api_secret=Env.CLOUDINARY_API_SECRET,
            secure=True
        )
    
    @staticmethod
    def test_connection() -> None:
        result = cloudinary.api.config()
        print('Cloudinary connection successful!')
        print(f'Cloud name: {result.get('cloud_name')}')
    
    @staticmethod
    async def create_image(image: UploadFile | FastAPIUploadFile) -> tuple[str, str]:
        file_bytes = await image.read()
        await image.seek(0)

        result = cloudinary.uploader.upload(
            io.BytesIO(file_bytes),
            folder=Env.CLOUDINARY_PFP_FOLDER,
            resource_type='image',
            public_id=str(uuid4()),
            overwrite=True
        )

        return (result['secure_url'], result['public_id'])

    @staticmethod
    async def destroy_image(public_id: str) -> None:
        cloudinary.uploader.destroy(public_id)
    
    def __new__(self):
        raise TypeError('ImageController class is not instantiable')