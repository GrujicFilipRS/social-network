<script lang="ts" setup>
import { ref } from 'vue';

import type { FollowWindowModeType as modeType } from '../interfaces/FollowWindowModeType' ;

const props = defineProps<{
    userId?: number,
}>();

const showRef = ref<boolean>(false);
const mode = ref<modeType>('FOLLOWING');

const showWindow = (modeToShow: modeType) => {
    showRef.value = true;
    mode.value = modeToShow;
}

defineExpose({ showWindow });

</script>

<template>
    <div
        v-show="showRef"
        class="follows-window-overlay"
    >
        <div class="follows-window">
            {{ props.userId }}
            {{ mode }}
            <button
                @click="showRef = false"
            >
                Exit
            </button>
        </div>


    </div>
</template>

<style>
@import url('./FollowWindow.css');
</style>