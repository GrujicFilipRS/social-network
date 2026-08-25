<script setup lang='ts'>

import { ref } from 'vue';
import type { Router } from 'vue-router';

import type { PostData } from '../interfaces/PostData';

import { GetPostPhotos } from '../functions/GetPostPhotos';
import { GetPostMiscData } from '../functions/GetPostMiscData';
import { LikePost, UnlikePost } from '../functions/LikePost';

import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue';

const toast = useToast();

const { postData, router } = defineProps<{postData: PostData, router: Router}>();
const likedByUser = ref<boolean>(false);
const firstImageSrc = ref<string | null>(null);
const numLikes = ref<number>(0);
const numComments = ref<number>(0);

const getMiscPostData = async () => {
    const data = await GetPostMiscData(postData.id);

    likedByUser.value = data.liked_by_user;
    numLikes.value = data.num_likes;
    numComments.value = data.num_comments;
}

const getFirstImage = async () => {
    firstImageSrc.value = (await GetPostPhotos(postData.id))[0]?.image_src ?? null;
}

getMiscPostData();
getFirstImage();

const shortenString = (
    input: string,
    maxLength: number,
    maxRows?: number
): string => {
    let result = input;

    if (maxRows) {
        const rows = result.split('\n');
        if (rows.length > maxRows) {
            result = rows.slice(0, maxRows).join('\n');
            return result + '...';
        }
    }

    if (result.length > maxLength) {
        return result.slice(0, maxLength) + '...';
    }

    return result;
};

const likeButtonLoading = ref<boolean>(false);
const clickLikeButton = () => {
    if (likedByUser.value) {
        UnlikePost(
            postData.id,
            () => {}, // No toast needed here
            (val: boolean) => likedByUser.value = val,
            (val: boolean) => likeButtonLoading.value = val,
            () => { numLikes.value -= 1 }
        );
    } else {
        LikePost(
            postData.id,
            (message: string) => { toast.add({
                severity: 'error',
                summary: 'An error occured',
                detail: message
            })},
            (val: boolean) => likedByUser.value = val,
            (val: number) => { numLikes.value += val }
        );
    }
}

const redirectToComments = () => router.push(`/post/${postData.id}#comments`)

</script>

<template>
    <Toast />
    <div class='post mb-4 p-2'>
        <div class='top' @click='() => router.push(`/post/${postData.id}`)'>
            <div class='ls-top'>
                <h3>{{ shortenString(postData.title, 25) }}</h3>
                <p style='white-space: pre-line;'>{{ shortenString(postData.body, 200, 4) }}</p>
            </div>

            <div class='rs-top' v-if='firstImageSrc'>
                <div
                    class='img-wrapper'
                    :style='{
                        backgroundImage: `url(${firstImageSrc})`
                    }'
                ></div>
            </div>
        </div>

        <div class='bottom mt-1'>
            <Button
                severity='secondary'
                class='p-button-sm'
                :icon='likedByUser ? `pi pi-thumbs-up-fill` : `pi pi-thumbs-up`'
                :label='String(numLikes)'
                :loading='likeButtonLoading'
                @click='clickLikeButton'
            />

            <Button
                severity='secondary'
                class='p-button-sm'
                icon='pi pi-comment'
                :label='String(numComments)'
                @click='redirectToComments'
            />
        </div>
    </div>
</template>

<style>
@import url('./ProfilePostView.css');
</style>