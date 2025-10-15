<script setup lang="ts">
import { useRouter } from 'vue-router';
import { verifyUser } from '../api';

const router = useRouter();

const userId = await verifyUser();
if (userId === -1) {
    router.push('/join');
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username: string | null = urlParams.get("user");

</script>

<template>
    {{ username }}
</template>

<style>
@import url('./Profile.css');
</style>