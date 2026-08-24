import type { DTO } from "./DTO";

export interface PostMiscResponse extends DTO {
    liked_by_user: boolean;
    num_likes: number;
    num_comments: number;
}