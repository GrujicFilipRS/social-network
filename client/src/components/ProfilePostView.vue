<script setup lang='ts'>
import type { PostData } from '../interfaces/PostData';

const { postData } = defineProps<{postData: PostData}>();

</script>

<template>
    {{ postData.title }}
</template>

<style>
@import url('./ProfilePostView.css');
</style>