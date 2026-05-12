import { type Notification } from '../interfaces/Notification';
import { Fetch } from '../api';

export const GetUnreadNotifications = async (): Promise<Notification[]> => {
    return Fetch('notifications/get_unread_notifications/')
    .then(async (response) => {
        if (response.ok) {
            const data = await response.json();
            return data as Notification[];
        } else {
            throw new Error('Failed to fetch notifications');
        }
    });
}