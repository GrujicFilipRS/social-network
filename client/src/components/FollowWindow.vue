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
}

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
            {{ JSON.stringify(userFollowers) }}
            {{ JSON.stringify(userFollows) }}
            <button @click="showRef = false">Exit</button>
        </div>
    </div>
</template>

<style>
@import url('./FollowWindow.css');
</style>