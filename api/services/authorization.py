from pydantic import BaseModel


class AuthorizationHeader(BaseModel):
    Authorization: str