import { Fetch } from '../api';

export const ReadNotification = async (notificationId: string): Promise<boolean> => {
    return await Fetch(`read_notification/${notificationId}`, { method: 'POST' })
    .then(async res => {
        if (!res.ok) {
            const errorData = await res.json();
            console.error(errorData.error || 'Failed to mark notification as read');
            return false;
        }

        return true;
    });
}