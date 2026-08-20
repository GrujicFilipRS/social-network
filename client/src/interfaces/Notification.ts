import type { UserData } from "./UserData";

export interface Notification {
    id: string;
    receiver: UserData;
    sender: UserData;
    message_txt: string;
    object_type: 'post' | 'like' | 'comment' | 'follow';
    object_id: string;
    received_at: string;
}