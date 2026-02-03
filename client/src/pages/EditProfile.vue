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
        <h1>Edit your profile</h1>

        <div class="pfp">
            <img
                :src="profileData.pfp_src"
                title="Click to change your profile picture"
            />
        </div>
        
        <div class="editor-wrapper name-editor-wrapper">
            <h1
                class="text-editor name-editor-text"
                title="Click to change name"
            >
                {{ profileData.nameText }}
            </h1>

            <button class="name-editor-button">✎</button>
        </div>

        <div class="editor-wrapper username-editor-wrapper">
            <h3
                class="text-editor username-editor-text"
                title="Click to change username"
            >
                {{ profileData.usernameText }}
            </h3>

            <button class="name-editor-button">✎</button>
        </div>
    </div>
</template>

<style>
@import url('./EditProfile.css');
</style>