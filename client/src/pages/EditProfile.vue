<script setup lang='ts'>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import {
    type EditProfileData,
    GetSelfProfileForEditing
}
from '../functions/GetSelfProfileForEditing';

import ChangePopup from '../components/ChangePopup.vue';

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

const displayProfileData = ref<EditProfileData>();
const actualProfileData = ref<EditProfileData>();
const setProfileDatas = async () => {
    const fetchedProfileData: EditProfileData[] = await GetSelfProfileForEditing();
    displayProfileData.value = fetchedProfileData[0]!;
    actualProfileData.value = fetchedProfileData[1]!;
}

await setProfileDatas();

const showPopup = ref<boolean>(false);
const popupTitle = ref<string>('');
const selectedElementValue = ref<string>('');

const loadUsernamePopup = () => {
    popupTitle.value = 'username';
    selectedElementValue.value = actualProfileData.value!.usernameText;
    showPopup.value = true;
}

const loadNamePopup = () => {
    popupTitle.value = 'name';
    selectedElementValue.value = actualProfileData.value!.nameText;
    showPopup.value = true;
}

</script>

<template>
    <div class='profile-editor'>
        <ChangePopup
            :title='popupTitle'
            :visible='showPopup'
            :original-value='selectedElementValue'
            :handle-close='() => showPopup = false'
        />

        <h1>Edit your profile</h1>

        <div class='pfp'>
            <img
                :src='displayProfileData!.pfp_src'
                title='Click to change your profile picture'
            />
        </div>
        
        <div class='editor-wrapper name-editor-wrapper'>
            <h1
                class='text-editor name-editor-text'
                title='Click to change name'
                @click='loadNamePopup'
            >
                {{ displayProfileData!.nameText }}
            </h1>

            <button class='name-editor-button'>✎</button>
        </div>

        <div class='editor-wrapper username-editor-wrapper'>
            <h3
                class='text-editor username-editor-text'
                title='Click to change username'
                @click='loadUsernamePopup'
            >
                {{ displayProfileData!.usernameText }}
            </h3>

            <button class='name-editor-button'>✎</button>
        </div>
    </div>
</template>

<style>
@import url('./EditProfile.css');
</style>