from io import BytesIO
from typing import BinaryIO

from PIL import Image, UnidentifiedImageError


class PhotoVerificationMethods:
    @staticmethod
    def verify_photo(stream: BytesIO) -> bool:
        MAX_SIZE = 15 * 1024 * 1024  # 15 MB
        ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "JPG"}

        stream.seek(0, 2)  # Seek to end
        size = stream.tell()
        stream.seek(0)

        if size == 0 or size > MAX_SIZE:
            return False

        try:
            img = Image.open(stream)
            img.verify()
            img_format = img.format
        except (UnidentifiedImageError, OSError, ValueError):
            return False

        if img_format not in ALLOWED_FORMATS:
            return False

        width, height = img.size

        if width > 6000 or height > 6000:
            return False

        if width < 300 or height < 300:
            return False

        stream.seek(0)
        return True
    
    @staticmethod
    def verify_pfp(stream: BinaryIO) -> bool:
        MAX_SIZE = 5 * 1024 * 1024  # 5MB
        ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}

        try:
            stream.seek(0, 2)
            size = stream.tell()

            if size > MAX_SIZE:
                return False

            stream.seek(0)

            with Image.open(stream) as img:
                img_format = img.format
                width, height = img.size

                if img_format not in ALLOWED_FORMATS:
                    return False

                if width > 512 or height > 512:
                    return False

                img.verify()

            stream.seek(0)

            return True

        except (UnidentifiedImageError, OSError, ValueError):
            return False