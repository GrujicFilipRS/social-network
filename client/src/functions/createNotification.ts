import { GetNotificationLink } from './GetNotificationLink';
import type { Notification } from '../interfaces/Notification';

import type { ToastServiceMethods } from 'primevue/toastservice';

export const createNotification = async (
    notification: Notification,
    toast: ToastServiceMethods,
    setLink: (link: string) => void
) => {
    toast.add({
        group: 'header-toast',
        severity: 'info',
        summary: 'Notification',
        detail: notification.message_txt,
        life: 3000
    });

    setLink(await GetNotificationLink(notification));
}