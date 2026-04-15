import type { CommentsData } from "./CommentsData";
import type { PhotoData } from "./PhotoData";
import type { UserData } from "./UserData";

export interface PostData {
    id: string;
    title: string;
    body: string;
    status: 'PUBLIC' | 'PRIVATE';
    created_at: string;
    likes: number;
    user: UserData;
    photos?: PhotoData[];
    comments?: CommentsData[];
    liked_by_user: boolean;
}