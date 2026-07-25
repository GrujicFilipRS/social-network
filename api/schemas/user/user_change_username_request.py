from pydantic import BaseModel, Field


class UserChangeUsernameRequest(BaseModel):
    new_username: str = Field(
        min_length=7,
        max_length=15,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
