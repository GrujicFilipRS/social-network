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
import Toast from 'primevue/toast';
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import Button from 'primevue/button';
import { useToast } from 'primevue';
import { EditUsername, EditName } from '../functions/UpdateProfile';
import { UploadPFP } from '../functions/UploadPFP';

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
const editFunction = ref<(username: string) => void>();

const toast = useToast();

const loadUsernamePopup = () => {
    popupTitle.value = 'username';
    selectedElementValue.value = actualProfileData.value!.usernameText;
    showPopup.value = true;
    editFunction.value = (username: string) => EditUsername(username, toast.add, (username: string) => {
        if (displayProfileData.value && actualProfileData.value) {
            displayProfileData.value.usernameText = username;
            actualProfileData.value.usernameText = username;
        }
    });
}

const loadNamePopup = () => {
    popupTitle.value = 'name';
    selectedElementValue.value = actualProfileData.value!.nameText;
    showPopup.value = true;
    editFunction.value = (username: string) => EditName(username, toast.add, (name: string) => {
        if (displayProfileData.value && actualProfileData.value) {
            displayProfileData.value.nameText = name;
            actualProfileData.value.nameText = name;
        }
    });
}

const imageUploadRef = ref();

const uploadImage = () => {
    if (imageUploadRef.value)
        imageUploadRef.value.upload();
}

const onUploadImage = (event: FileUploadUploaderEvent) => {
    const files = event.files;
    const image: File = Array.isArray(files) ? files[0]! : files;

    UploadPFP(image, toast.add);
} 

</script>

<template>
    <div class='profile-editor'>
        <Toast />

        <ChangePopup
            :title='popupTitle'
            :visible='showPopup'
            :original-value='selectedElementValue'
            :handle-close='() => showPopup = false'
            :edit-function='editFunction'
            :refresh-function='setProfileDatas'
        />

        <h1>Edit your profile</h1>

        <div class='pfp'>
            <img
                :src='displayProfileData!.pfp_src'
                title='Click to change your profile picture'
            />
        </div>

        <FileUpload
            ref='imageUploadRef'
            mode='basic'
            accept='image/*'
            :customUpload='true'
            @uploader='onUploadImage'
        />

        <Button label='Upload' @click='uploadImage' severity='secondary' />
        
        <div class='editor-wrapper name-editor-wrapper'>
            <h2
                class='text-editor name-editor-text'
                title='Click to change name'
                @click='loadNamePopup'
            >
                {{ displayProfileData!.nameText }}
            </h2>

            <button
                class='name-editor-button'
                @click='loadNamePopup'
            >
                ✎
            </button>
        </div>

        <div class='editor-wrapper username-editor-wrapper'>
            <h3
                class='text-editor username-editor-text'
                title='Click to change username'
                @click='loadUsernamePopup'
            >
                {{ displayProfileData!.usernameText }}
            </h3>

            <button
                class='name-editor-button'
                @click='loadUsernamePopup'
            >
                ✎
            </button>
        </div>
    </div>
</template>

<style>
@import url('./EditProfile.css');
</style>