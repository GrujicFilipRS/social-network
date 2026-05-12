<script setup lang='ts'>
import type { Notification } from '../interfaces/Notification';

defineProps<{
    notification: Notification;
}>();

</script>

<template>
    <div class='notification-card'>
        <div class='notification-content'>
            <p>{{ notification.message_txt }}</p>
            <span class='notification-time'>
                {{ new Date(notification.received_at).toLocaleString('sr-RS') }}
            </span>
        </div>
    </div>
</template>