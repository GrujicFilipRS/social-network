export interface Notification {
    id: string;
    message_txt: string;
    object_type: 'post' | 'like' | 'comment' | 'follow';
    object_id: string;
    received_at: string;
}