from uuid import UUID

from pydantic import BaseModel


class FollowCreateRequest(BaseModel):
    to_follow_id: UUID