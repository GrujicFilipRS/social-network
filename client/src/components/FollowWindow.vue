<script lang="ts" setup>
import { onMounted, ref } from 'vue';

import { GetUserFollowers } from '../functions/GetUserFollowers';
import { GetUserFollows } from '../functions/GetUserFollows';

import type { FollowWindowModeType as modeType } from '../interfaces/FollowWindowModeType' ;
import type { FollowsData } from '../interfaces/FollowData';
// import type { FollowsData } from '../interfaces/FollowData';

const props = defineProps<{
    userId?: number,
}>();

const showRef = ref<boolean>(false);
const mode = ref<modeType>('FOLLOWING');

const showWindow = (modeToShow: modeType) => {
    showRef.value = true;
    mode.value = modeToShow;
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
                    <button
                        class="follows-btn"
                    >Follows</button>

                    <button
                        class="followers-btn"
                    >Followers</button>
                </div>

                <button
                    class="close-follows-btn"
                    @click="closeWindow"
                >✖</button>
            </div>
        </div>
    </div>
</template>

<style>
@import url('./FollowWindow.css');
</style>