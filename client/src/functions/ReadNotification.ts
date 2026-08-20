import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const ReadNotification = async (notificationId: string): Promise<boolean> => {
    return await axios.post(`notifications/read_notification/${notificationId}`)
    .then(async res => {
        const data: DTO = res.data;

        if (!data.success) {
            console.error(data.message || 'Failed to mark notification as read');
            return false;
        }

        return true;
    });
}