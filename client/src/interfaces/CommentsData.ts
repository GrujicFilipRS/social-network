import type { UserData } from "./UserData";

export interface CommentsData {
    id: string;
    body: string;
    post_id: string;
    comment_id: string | null;
    creator: UserData;
    commented_at: string;
}