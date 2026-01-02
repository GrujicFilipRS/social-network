<script setup lang="ts">

import { useRouter } from 'vue-router';

import { verifyUser } from '../api';

const router = useRouter();

const userId = await verifyUser();
if (!userId) {
    router.push('/join');
}

</script>

<template>

<h1>Feed</h1>

</template>