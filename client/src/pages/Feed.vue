<script setup lang='ts'>

import { useRouter } from 'vue-router';

import { verifyUser, UserUnverifiedError } from '../api';

const router = useRouter();

await verifyUser().catch((_: UserUnverifiedError) => router.push('/'));

</script>

<template>

<h1>Feed</h1>

</template>