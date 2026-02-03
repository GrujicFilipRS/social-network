<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import { GetSelfProfileForEditing, type EditProfileData } from '../functions/GetSelfProfileForEditing';

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

const profileData = ref<EditProfileData>(
    await GetSelfProfileForEditing() as EditProfileData
);

if (profileData.value.status === 404) {
    router.push('/feed');
}

</script>

<template>
    <div class="profile-editor">
        <div class="pfp">
            <img :src="profileData.pfp_src" />
        </div>

        <h1 class="name-editor">{{ profileData.name }}</h1>
        <p class="username-editor">{{ profileData.username }}</p>
    </div>
</template>

<style>
@import url('./EditProfile.css');
</style>