<script setup lang='ts'>
import type { Notification } from '../interfaces/Notification';

const props = defineProps<{
    notification: Notification;
}>();

</script>

<template>
    <div class='notification-card'>
        <div class='notification-content'>
            <p>{{ notification.message_txt }}</p>
            <span class='notification-time'>{{ notification.received_at }}</span>
        </div>
    </div>
</template>