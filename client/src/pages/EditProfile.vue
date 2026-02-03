<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import type { ProfileData } from '../interfaces/ProfileData';
import { GetSelfProfile } from '../functions/GetProfile';

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

interface FetchStatusData {
    status: number;
    data: ProfileData;
}

const fetchData = ref<FetchStatusData>(
    await GetSelfProfile() as FetchStatusData
);

if (fetchData.value.status === 404) {
    router.push('/feed');
}

const profileData: ProfileData = ref<ProfileData>(fetchData.value.data).value;
</script>

<template>
    <div class="profile-editor">
        <div class="pfp">
            <img :src="profileData.pfp_src ?? '/default-pfp.png'" />
        </div>
    </div>
</template>

<style>
@import url('./EditProfile.css');
</style>