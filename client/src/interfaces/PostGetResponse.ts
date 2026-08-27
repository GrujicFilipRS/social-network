import type { DTO } from "./DTO";
import type { PostData } from "./PostData";

export interface PostGetResponse extends DTO {
    post: PostData | null;
}