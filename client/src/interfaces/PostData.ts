import type { UserData } from "./UserData";

export interface PostData {
    id: string;
    title: string;
    body: string;
    status: 'PUBLIC' | 'PRIVATE';
    created_at: string;
    user: UserData;
}