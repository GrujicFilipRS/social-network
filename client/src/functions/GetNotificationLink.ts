import type { Notification } from '../interfaces/Notification';
import { GetFollowerIdFromFollowId } from './GetFollowerIdFromFollowId';
import { GetPostIdFromCommentId } from './GetPostIdFromCommentId';
import { GetPostIdFromLikeId } from './GetPostIdFromLikeId';

export const GetNotificationLink = (notification: Notification): string => {
    switch (notification.object_type) {
        case 'post':
            return `/post?post_id=${notification.object_id}`;
        case 'like':
            return `/post?post_id=${GetPostIdFromLikeId(notification.object_id)}`;
        case 'comment':
            return (
                `/post?post_id=${
                    GetPostIdFromCommentId(notification.object_id)
                }#comment-${notification.object_id}`
            );
        case 'follow':
            return `/profile?user_id=${GetFollowerIdFromFollowId(notification.object_id)}`;
    }
}