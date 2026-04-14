<script lang='ts' setup>
import { onMounted, ref } from 'vue';

import { GetUserFollowers } from '../functions/GetUserFollowers';
import { GetUserFollows } from '../functions/GetUserFollows';

import type { FollowWindowModeType as modeType } from '../interfaces/FollowWindowModeType' ;
import type { FollowsData } from '../interfaces/FollowData';

import Dialog from 'primevue/dialog';
import Avatar from 'primevue/avatar';

const props = defineProps<{
    userId?: string,
}>();

const showRef = ref<boolean>(false);
const mode = ref<modeType>('FOLLOWING');
const followsTextClass = ref<'mode-active' | ''>('mode-active');
const followersTextClass = ref<'mode-active' | ''>('');

const showWindow = (modeToShow: modeType) => {
    showRef.value = true;
    setWindowMode(modeToShow);
};

const setWindowMode = (modeToShow: modeType) => {
    mode.value = modeToShow;
    if (modeToShow == 'FOLLOWING') {
        followsTextClass.value = 'mode-active';
        followersTextClass.value = '';
    } else {
        followsTextClass.value = '';
        followersTextClass.value = 'mode-active';
    }
};

const userFollowers = ref<FollowsData | null>(null);
const userFollows = ref<FollowsData | null>(null);
onMounted(async () => {
    userFollowers.value = await GetUserFollowers(props.userId!) as FollowsData;
    userFollows.value = await GetUserFollows(props.userId!) as FollowsData;
});

defineExpose({ showWindow });

</script>

<template>
    <Dialog
        v-model:visible='showRef'
        modal
        class='follows-window-overlay'
    >
        <div class='follows-window-header'>
            <span
                :class='followsTextClass'
                @click='setWindowMode("FOLLOWING")'
            >Following</span>

            <span
                :class='followersTextClass'
                @click='setWindowMode("FOLLOWERS")'
            >Followers</span>

        </div>
        
        <div class='user-list'>
            <div
                v-for='user in mode == "FOLLOWING" ? userFollows!.users : userFollowers!.users'
                :key='user.id'
                class='user-list-item'
            >
                <Avatar
                    :image='user.pfp ?? "/default-pfp.png"'
                    shape='circle'
                />

                <a class='username' :href='`/profile?user=${user.username}`'>{{ user.username }}</a>
            </div>
        </div>

        <p
            v-if='mode == "FOLLOWING" ?
            userFollows!.users.length === 0 :
            userFollowers!.users.length === 0'
        >No users found</p>
    </Dialog>
</template>

<style>
@import url('./FollowWindow.css');
</style>