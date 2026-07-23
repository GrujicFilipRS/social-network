from io import BytesIO
import unicodedata

from pydantic import BaseModel, Field, field_validator, model_validator

from utils import PostLiterals


class PostCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=45)
    body: str | None = Field(default='')
    status: str
    image_streams: list[BytesIO] = Field(default_factory=list)

    model_config = {
        'arbitrary_types_allowed': True
    }

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not all(c.isprintable() or c in '\n\r\t' for c in value):
            raise ValueError('Title contains invalid characters')

        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in value
        ):
            raise ValueError('Title contains control characters')

        return value

    @field_validator('body')
    @classmethod
    def validate_body(cls, value: str | None) -> str:
        value = (value or '').strip()

        if len(value) > 280:
            raise ValueError('Body too long')

        if value.count('\n') > 10:
            raise ValueError('Body contains too many lines')

        if not all(c.isprintable() or c in '\n\r\t' for c in value):
            raise ValueError('Body contains invalid characters')

        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in value
        ):
            raise ValueError('Body contains control characters')

        dangerous = (
            '<script',
            '</script',
            'javascript:',
            'onerror=',
            'onload=',
        )

        if any(s in value.lower() for s in dangerous):
            raise ValueError('Body contains forbidden content')

        return value

    @field_validator('status')
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().upper()

        if value not in PostLiterals.LIST_LITS:
            raise ValueError('Invalid status')

        return value

    @model_validator(mode='after')
    def validate_images(self):
        if len(self.image_streams) > 10:
            raise ValueError('Too many images')

        return self