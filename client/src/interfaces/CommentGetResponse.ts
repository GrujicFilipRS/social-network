import type { CommentsData } from "./CommentsData";
import type { DTO } from "./DTO";

export interface CommentGetResponse extends DTO {
    comment: CommentsData | null;
}