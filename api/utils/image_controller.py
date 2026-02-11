import cloudinary, io
import cloudinary.api, cloudinary.uploader
from fastapi import UploadFile
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
        try:
            result = cloudinary.api.config()
            print('Cloudinary connection successful!')
            print(f'Cloud name: {result.get('cloud_name')}')
        except Exception as e:
            print(f'Cloudinary connection unsuccessful: {e}')
    
    @staticmethod
    async def create_pfp(image: UploadFile) -> tuple[str, str]:
        file_bytes = await image.read()

        result = cloudinary.uploader.upload(
            io.BytesIO(file_bytes),
            folder=Env.CLOUDINARY_PFP_FOLDER,
            resource_type='image',
            public_id=image.filename.split('.')[0],
            overwrite=True
        )

        return (result['secure_url'], result['public_id'])

    @staticmethod
    async def destroy_pfp(public_id: str) -> None:
        cloudinary.uploader.destroy(public_id)
    
    def __new__():
        raise TypeError('CloudinaryController class is not instantiable')