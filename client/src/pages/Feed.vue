<script setup lang="ts">

import { useRouter, useRoute } from 'vue-router';
import { watch } from 'vue';

import { verifyUser } from '../api';

const router = useRouter();
const route = useRoute();

async function verifyAndRedirect() {
    const userId = await verifyUser();
    if (userId == -1) {
        router.push('/nigga');
    }
}

verifyAndRedirect();

watch(() => route.fullPath, verifyAndRedirect);

</script>

<template>

<h1>Feed</h1>

</template>