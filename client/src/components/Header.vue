<script lang='ts' setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser, createWebSocket } from '../api';
import { createNotification } from '../functions/createNotification';
import { HandleLogout } from '../functions/HandleLogout';
import { eventBus } from '../events';

import Drawer from 'primevue/drawer';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const toast = useToast();

const headerVisible = ref<boolean>(false);
const drawerVisible = ref<boolean>(false);
const pfpSource = ref<string>('/default-pfp.png');
const websocket = ref<WebSocket | null>(null);

const initiateHeader = async () => {
    verifyUser().then(res => {
        if (res.statusCode !== 401) headerVisible.value = true;
        pfpSource.value = res.result.user?.pfp ?? '/default-pfp.png';
    });

    websocket.value = createWebSocket('notifications/', (event) => {
        createNotification(
            event.data,
            toast
        );
    });
}

initiateHeader();

onMounted(() => {
    eventBus.on('header-update', initiateHeader);
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
    <Toast position='bottom-right' />

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
                style='width: 100%;'
                @click='() => { router.push("/profile"); drawerVisible = false; }'
            />

            <Button
                class='header-btn'
                icon='pi pi-user-edit'
                label='Edit profile'
                severity='secondary'
                style='width: 100%;'
                @click='() => { router.push("/edit_profile"); drawerVisible = false; }'
            />

            <Button
                class='header-btn'
                icon='pi pi-sign-out'
                label='Log out'
                severity='danger'
                style='width: 100%;'
                @click='Logout'
            />
        </Drawer>
    </div>
</template>

<style>
@import url('./Header.css');
</style>