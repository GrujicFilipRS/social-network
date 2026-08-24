from ..shared.dto import DTO


class PostMiscResponse(DTO):
    liked_by_user: bool = False
    num_likes: int = 0
    num_comments: int = 0
    
    @staticmethod
    def ok(liked_by_user: bool, num_likes: int, num_comments: int, message: str | None = None):
        return PostMiscResponse(
            success = True,
            message = message,
            liked_by_user = liked_by_user,
            num_likes = num_likes,
            num_comments = num_comments
        )
    
    @staticmethod
    def error(message: str):
        return PostMiscResponse(
            success = False,
            message = message,
        )