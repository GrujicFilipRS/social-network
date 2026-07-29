from models import Comment

from ..shared.dto import DTO
from .comment_dto import CommentDTO


class CommentGetResponse(DTO):
    comment: CommentDTO | None
    
    @staticmethod
    def ok(comment: Comment | CommentDTO, message: str | None = None) -> CommentDTO:
        return CommentDTO(
            success = True,
            message = message,
            comment = CommentDTO.to_dto(comment)
        )
    
    @staticmethod
    def error(message: str) -> CommentDTO:
        return CommentDTO(
            success = False,
            message = message,
            comment = None
        )