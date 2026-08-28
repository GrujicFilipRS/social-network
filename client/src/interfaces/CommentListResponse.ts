import type { CommentsData } from "./CommentsData";
import type { DTO } from "./DTO";

export interface CommentListResponse extends DTO {
    comments: CommentsData[];
}