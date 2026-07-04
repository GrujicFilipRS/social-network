from typing import Optional

from pydantic import BaseModel, Field

class UserRegistrationRequest(BaseModel):
    username: str = Field(
        min_length=7,
        max_length=15,
        pattern=r"^[a-zA-Z0-9_]+$"
    )

    password: str = Field(
        min_length=8,
        max_length=14
    )

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=r"^[\p{L}][\p{L}\p{M}'\-.\s]*$"
    )