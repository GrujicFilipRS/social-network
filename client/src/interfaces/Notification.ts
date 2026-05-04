export interface Notification {
    message_txt: string;
    object_type: 'post' | 'like' | 'comment';
    object_id: string;
}