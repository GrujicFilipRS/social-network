import type { DTO } from "./DTO";
import type { PostData } from "./PostData";
import type { UserData } from "./UserData";

export interface UserProfileGetResponse extends DTO {
    user: UserData | null;
    num_followers: number;
    num_follows: number;
    user_followed: boolean;
    posts: PostData[];
}