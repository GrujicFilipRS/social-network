<script lang="ts" setup>
import { onMounted, ref } from 'vue';

import { GetUserFollowers } from '../functions/GetUserFollowers';
import { GetUserFollows } from '../functions/GetUserFollows';

import type { FollowWindowModeType as modeType } from '../interfaces/FollowWindowModeType' ;
import type { FollowsData } from '../interfaces/FollowData';

import FollowBox from './FollowBox.vue';

const props = defineProps<{
    userId?: number,
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

const closeWindow = () => {
    showRef.value = false;
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
    <div
        v-show="showRef"
        class="follows-window-overlay"
    >
        <div class="follows-window">
            <div class="follows-header">
                <div class="lside-follows-header">
                    <p
                        :class="followsTextClass"
                        @click="setWindowMode('FOLLOWING')"
                    >
                        Follows
                    </p>

                    <p
                        :class="followersTextClass"
                        @click="setWindowMode('FOLLOWERS')"
                    >
                        Followers
                    </p>
                </div>

                <button
                    class="close-follows-btn"
                    @click="closeWindow"
                >✖</button>
            </div>

            <div
                class="follows-list"
                v-show="mode == 'FOLLOWING'"
            >
                <FollowBox
                    v-for="(user, index) in userFollows?.users"
                    :key="user.id || index"
                    :user="user"
                />
            </div>

            <div
                class="follows-list"
                v-show="mode == 'FOLLOWERS'"
            >
                <FollowBox
                    v-for="(user, index) in userFollowers?.users"
                    :key="user.id || index"
                    :user="user"
                />
            </div>
        </div>
    </div>
</template>

<style>
@import url('./FollowWindow.css');
</style>