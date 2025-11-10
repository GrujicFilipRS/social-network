<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import type { ProfileData } from '../interfaces/ProfileData';
import { GetSelfProfile } from '../functions/GetProfile';

const router = useRouter();

const userId = await verifyUser();
if (userId === -1) {
    router.push('/join');
}

const fetchData = ref<{status: number, data: ProfileData}>(await GetSelfProfile() as {status: number, data: ProfileData});

if (fetchData.value.status === 404) {
    router.push('/feed');
}

const data: ProfileData = ref<ProfileData>(fetchData.value.data).value;
</script>

<template>
    <div class="profile-editor">
        
    </div>
</template>