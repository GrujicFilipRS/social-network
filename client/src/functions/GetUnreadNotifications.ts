import { type Notification } from '../interfaces/Notification';
import { type NotificationListResponse } from '../interfaces/NotificationListResponse';
import axios from 'axios';

export const GetUnreadNotifications = async (): Promise<Notification[]> => {
    return axios.get('notifications/get_unread_notifications/')
    .then(async res => {
        const data: NotificationListResponse = res.data;

        if (data.success) {
            return data.notifications;
        } else {
            console.error('Failed to fetch notifications');
            return [];
        }
    })
    .catch((_) => {
        console.error('Failed to fetch notifications');
        return [];
    })
}