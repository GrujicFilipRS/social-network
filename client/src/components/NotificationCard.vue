<script setup lang='ts'>
import { GetNotificationText } from '../functions/GetNotificationText';
import { ReadNotification } from '../functions/ReadNotification';
import type { Notification } from '../interfaces/Notification';

import Button from 'primevue/button';

const props = defineProps<{
    notification: Notification;
    reloadNotifications: () => void;
}>();

const handleRead = async () => {
    await ReadNotification(props.notification.id).then(props.reloadNotifications);
}

</script>

<template>
    <div class='notification-card'>
        <div class='notification-content flex align-items-center justify-content-between'>
            <div class='lside-not'>
                <p>{{ GetNotificationText(notification) }}</p>
                <span class='notification-time'>
                    {{ new Date(notification.received_at).toLocaleString('sr-RS') }}
                </span>
            </div>
            
            <Button
                severity='secondary'
                size='small'
                icon='pi pi-eye'
                title='Mark as read'
                @click='handleRead()'
            />
        </div>
    </div>
</template>