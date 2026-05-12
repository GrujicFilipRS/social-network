<script lang='ts' setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser, createWebSocket } from '../api';
import type { Notification } from '../interfaces/Notification';
import { createNotification } from '../functions/createNotification';
import { GetUnreadNotifications } from '../functions/GetUnreadNotifications';
import { HandleLogout } from '../functions/HandleLogout';
import { eventBus } from '../events';

import NotificationCard from './NotificationCard.vue';

import Drawer from 'primevue/drawer';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const toast = useToast();

const headerVisible = ref<boolean>(false);
const drawerVisible = ref<boolean>(false);
const notificationDrawerVisible = ref<boolean>(false);
const pfpSource = ref<string>('/default-pfp.png');
const websocket = ref<WebSocket | null>(null);
const notificationLink = ref<string>('/');
const unreadNotifications = ref<Notification[]>([]);

const initiateHeader = async () => {
    verifyUser().then(res => {
        if (res.statusCode !== 401) headerVisible.value = true;
        pfpSource.value = res.result.user?.pfp ?? '/default-pfp.png';
    });

    websocket.value = createWebSocket('notifications/', async (event) => {
        const notificationData = JSON.parse(event.data) as Notification;

        await createNotification(
            notificationData,
            toast,
            (val: string) => notificationLink.value = val
        );
    });
}

initiateHeader();

onMounted(async () => {
    eventBus.on('header-update', initiateHeader);
    
    unreadNotifications.value = await GetUnreadNotifications();
});

onUnmounted(() => {
    eventBus.off('header-update', initiateHeader);
});

const Logout = () => {
    HandleLogout(
        router,
        () => {
            drawerVisible.value = false;
            headerVisible.value = false;
        }
    );
}

</script>

<template>
    <Toast
        group='header-toast'
        position='bottom-right'
        style='cursor: pointer'
        @click='() => router.push(notificationLink)'
    />

    <div id='header' v-if='headerVisible'>
        <Avatar
            class='avatar'
            :image='pfpSource'
            @click='drawerVisible = true'
            shape='circle'
            style='width: 50px; height: 50px; cursor: pointer;'
        />

        <Drawer
            v-model:visible='drawerVisible'
            position='right'
            header='Quick options'
            class='header-drawer'
        >
            <Button
                class='header-btn'
                icon='pi pi-user'
                label='View profile'
                severity='secondary'
                @click='() => { router.push("/profile"); drawerVisible = false; }'
            />

            <Button
                class='header-btn'
                icon='pi pi-user-edit'
                label='Edit profile'
                severity='secondary'
                @click='() => { router.push("/edit_profile"); drawerVisible = false; }'
            />

            <Button
                class='header-btn'
                icon='pi pi-bell'
                severity='secondary'
                :label='`Unread notifications (${unreadNotifications.length})`'
                @click='() => { notificationDrawerVisible = true; drawerVisible = false; }'
            />

            <Button
                class='header-btn'
                icon='pi pi-sign-out'
                label='Log out'
                severity='danger'
                @click='Logout'
            />
        </Drawer>

        <Drawer
            v-model:visible='notificationDrawerVisible'
            position='right'
            header='Unread notifications'
            class='header-drawer'
        >
            <div v-if='unreadNotifications.length === 0' class='no-notifications'>
                No unread notifications.
            </div>

            <NotificationCard
                v-for='notification in unreadNotifications'
                :key='notification.object_id'
                :notification='notification'
            />
        </Drawer>
    </div>
</template>

<style>
@import url('./Header.css');
</style>