<script setup lang="ts">
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