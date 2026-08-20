import type { Notification } from "../interfaces/Notification";

export const GetNotificationText = (notification: Notification) => {
    let message: string = 'You received a new notification';
    const sender = notification.sender.name ?? notification.sender.username;

    switch(notification.object_type) {
        case "post":
            message = `${sender} just created a new post`;
            break;
        case "like":
            message = `${sender} just liked your post`;
            break;
        case "comment":
            message = `${sender} just commented on your post`;
            break;
        case "follow":
            message = `${sender} just followed you`;
            break;
    }

    return message;
}