<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { verifyUser } from '../api';

import { GetProfile } from '../functions/GetProfile';

const router = useRouter();

const userId = await verifyUser();
if (userId === -1) {
    router.push('/join');
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username: string | null = urlParams.get("user");

const data = ref(await GetProfile(username));

const firstRow: string = data.value.user_name ? data.value.user_name : data.value.username;
const secondRow: string | null= data.value.user_name ? data.value.username : null;

</script>

<template>
    <div class="profile-info">
        <div class="lside-info">
            <div class="pfp">
                <img :src="data.pfp_src || '/default-pfp.png'" />
            </div>

            <div class="names">
                <h2>{{ firstRow }}</h2>
                <p>{{ secondRow }}</p>
            </div>
        </div>
    </div>

    <div class="posts">

    </div>
</template>

<style>
@import url('./Profile.css');
</style>