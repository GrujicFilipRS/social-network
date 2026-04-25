import type { ToastServiceMethods } from 'primevue/toastservice';

export const createNotification = (message: string, toast: ToastServiceMethods) => {
    toast.add({
        severity: 'info',
        summary: 'Notification',
        detail: message,
        life: 3000
    });
}