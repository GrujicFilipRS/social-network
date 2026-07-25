from pydantic import BaseModel, Field


class SetNameRequest(BaseModel):
    new_name: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[\p{L}][\p{L}\p{M}'\-.\s]*$"
    )