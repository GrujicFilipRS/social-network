import type { Notification } from '../interfaces/Notification';
import { GetPostIdFromCommentId } from './GetPostIdFromCommentId';
import { GetPostIdFromLikeId } from './GetPostIdFromLikeId';
import { GetFollowerUsernameFromFollowId } from './GetFollowerUsernameFromFollowId';

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
            const followerUsername = await GetFollowerUsernameFromFollowId(notification.object_id);
            return `/profile?user=${followerUsername}`;
    }
}