<script setup lang='ts'>
import Header from './components/Header.vue';
</script>

<template>
    <suspense>
        <div id='view'>
            <Header />
            <router-view />
        </div>
    </suspense>
</template>

<style scoped></style>
