export interface Notification {
    message_txt: string;
    object_type: 'post' | 'like' | 'comment' | 'follow';
    object_id: string;
}