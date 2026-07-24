from pydantic import BaseModel, Field


class PostEditRequest(BaseModel):
    title: str = Field(min_length=3, max_length=45)
    body: str | None = Field(default='')
    status: str