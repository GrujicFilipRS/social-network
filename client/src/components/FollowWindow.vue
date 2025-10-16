<script lang="ts" setup>

const props = defineProps<{
    userId?: number
}>();

</script>

<template>
    <div class="follows-window">
        {{ props.userId }}
    </div>
</template>

<style>
@import url('./FollowWindow.css');
</style>