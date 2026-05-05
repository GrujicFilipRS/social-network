import type { Notification } from '../interfaces/Notification';
import { GetFollowerIdFromFollowId } from './GetFollowerIdFromFollowId';
import { GetPostIdFromCommentId } from './GetPostIdFromCommentId';
import { GetPostIdFromLikeId } from './GetPostIdFromLikeId';

export const GetNotificationLink = async (notification: Notification): Promise<string> => {
    let postId = '';
    switch (notification.object_type) {
        case 'post':
            return `/post?post_id=${notification.object_id}`;
        case 'like':
            postId = await GetPostIdFromLikeId(notification.object_id);
            return `/post?post_id=${postId}`;
        case 'comment':
            postId = await GetPostIdFromCommentId(notification.object_id);
            return `/post?post_id=${postId}#comment-${notification.object_id}`;
        case 'follow':
            return `/profile?user_id=${GetFollowerIdFromFollowId(notification.object_id)}`;
    }
}