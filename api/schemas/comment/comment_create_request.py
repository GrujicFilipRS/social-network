import unicodedata
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel


def body_valid(body: str) -> str:
    if not body:
        raise ValueError('Body cannot be empty')
    
    MIN_BODY_LENGTH = 1
    MAX_BODY_LENGTH = 80
    
    if len(body) < MIN_BODY_LENGTH or len(body) > MAX_BODY_LENGTH:
        raise ValueError(f'Body must be between {MIN_BODY_LENGTH} and {MAX_BODY_LENGTH} characters')
    
    MAX_BODY_LINES = 3
    if body.count('\n') > MAX_BODY_LINES:
        raise ValueError(f'Body cannot have more than {MAX_BODY_LINES} lines')
    
    if not all(c.isprintable() or c in '\n\r\t' for c in body):
        raise ValueError('Body contains invalid characters')
    
    DANGEROUS_SUBSTRINGS = (
        '<script',
        '</script',
        'javascript:',
        'onerror=',
        'onload=',
        '<iframe',
        '</iframe',
    )
    
    lower_body = body.lower()
    if any(x in lower_body for x in DANGEROUS_SUBSTRINGS):
        raise ValueError('Body contains dangerous substrings')
    
    if any(
        unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
        for c in body
    ):
        raise ValueError('Body contains control characters')
    
    return body


class CommentCreateRequest(BaseModel):
    post_id: UUID
    comment_id: UUID | None = None
    
    body: Annotated[str, AfterValidator(body_valid)]