<script setup lang='ts'>
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
        <div class='notification-content'>
            <p>{{ notification.message_txt }}</p>
            <span class='notification-time'>
                {{ new Date(notification.received_at).toLocaleString('sr-RS') }}
            </span>

            <Button
                severity='secondary'
                size='small'
                icon='pi pi-eye'
                @click='handleRead()'
            />
        </div>
    </div>
</template>