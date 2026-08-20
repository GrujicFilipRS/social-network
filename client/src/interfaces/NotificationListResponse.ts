import type { DTO } from "./DTO";
import type { Notification } from "./Notification";

export interface NotificationListResponse extends DTO {
    notifications: Notification[];
}