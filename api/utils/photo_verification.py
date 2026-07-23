from io import BytesIO
from PIL import Image


class PhotoVerificationMethods:
    @staticmethod
    def verify_photo(stream: BytesIO) -> bool:
        MAX_SIZE = 15 * 1024 * 1024  # 15 MB
        ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "JPG"}

        try:
            stream.seek(0, 2)  # Seek to end
            size = stream.tell()
            stream.seek(0)
        except Exception:
            return False

        if size == 0 or size > MAX_SIZE:
            return False

        try:
            img = Image.open(stream)
            img.verify()
            img_format = img.format
        except Exception:
            return False

        if img_format not in ALLOWED_FORMATS:
            return False

        try:
            stream.seek(0)
            img = Image.open(stream)
            width, height = img.size
        except Exception:
            return False

        if width > 6000 or height > 6000:
            return False

        if width < 300 or height < 300:
            return False

        stream.seek(0)
        return True