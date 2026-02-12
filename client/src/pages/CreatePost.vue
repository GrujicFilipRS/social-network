<script lang='ts' setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { CreatePost, VerifyImages } from '../functions/CreatePost';

import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import Select from 'primevue/select';
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const router = useRouter();

const toast = useToast();
const imageUploadRef = ref();
const uploadedImages = ref<File[]>([]);
const imagesValid = ref<boolean>(true);
const postLoading = ref<boolean>(false);

const title = ref<string>('');
const body = ref<string>('');
const status = ref<'Private' | 'Public'>('Public');

const onUploadImages = (event: FileUploadUploaderEvent) => {
    const files = Array.isArray(event.files) ? event.files : [event.files];

    const [isValid, errorMessage] = VerifyImages(files);

    if (!isValid) {
        toast.add({ severity: 'error', summary: 'Error', detail: errorMessage });
        imagesValid.value = false;
        return;
    }

    uploadedImages.value.push(...files);
    imageUploadRef.value.clear();
};

const submitPost = () => {
    if (imageUploadRef.value)
        imageUploadRef.value.upload();

    if (!imagesValid.value)
        return;

    CreatePost(
        title.value,
        body.value,
        status.value,
        uploadedImages.value,
        (title: string, message: string, severity?: 'success' | 'info' | 'warn' | 'error') => {
            toast.add(
                { severity: severity || 'info', summary: title, detail: message, life: 3000 }
            );
        },
        (route: string) => router.push(route),
        (val: boolean) => postLoading.value = val
    );
}

</script>

<template>
    <Toast />

    <div class='flex flex-col gap-10 w-[60%]'>
        <h1>Create Post</h1>

        <div class='flex flex-col gap-5'>
            <InputText
                v-model='title'
                placeholder='Title'
            />

            <Textarea
                v-model='body'
                placeholder='What do you want to talk about?'
                style='resize: none'
                :rows='6'
            />

            <Select
                v-model='status'
                :options='["Public", "Private"]'
            />

            <FileUpload
                ref='imageUploadRef'
                mode='basic'
                :custom-upload='true'
                accept='.jpg,.jpeg,.png,.webp'
                :multiple='true'
                @uploader='onUploadImages'
            />

            <Button
                label='Post'
                @click='submitPost'
                :loading='postLoading'
            />
        </div>
    </div>
</template>