<script setup lang="ts">

import { useRouter } from 'vue-router';

import { verifyUser } from '../api';

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

</script>

<template>

<h1>Feed</h1>

</template>