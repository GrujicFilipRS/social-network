<script setup lang='ts'>
import { ref } from 'vue';

import type { PostData } from '../interfaces/PostData';

import { LikePost, UnlikePost } from '../functions/LikePost';

import Button from 'primevue/button';

const { postData } = defineProps<{postData: PostData}>();

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
    if (postData.liked_by_user) {
        UnlikePost(
            postData.id,
            () => {}, // No toast needed here
            (val: boolean) => postData.liked_by_user = val,
            (val: boolean) => likeButtonLoading.value = val,
            () => postData.likes -= 1
        );
    } else {
        LikePost(
            postData.id,
            () => {},
            (val: boolean) => postData.liked_by_user = val,
            (val: boolean) => likeButtonLoading.value = val,
            () => postData.likes += 1
        );
    }
}

</script>

<template>
    <div class='post mb-4'>
        <div class='top'>
            <div class='ls-top'>
                <h3>{{ shortenString(postData.title, 25) }}</h3>
                <p style='white-space: pre-line;'>{{ shortenString(postData.body, 200, 4) }}</p>
            </div>

            <div class='rs-top' v-if='postData.photos.length > 0'>
                <div
                    class='img-wrapper'
                    :style='{
                        backgroundImage: `url(${postData.photos[0]!.image_src})`
                    }'
                />
            </div>
        </div>

        <div class='bottom mt-1'>
            <Button
                severity='secondary'
                class='p-button-sm'
                :icon='postData.liked_by_user ? `pi pi-thumbs-up-fill` : `pi pi-thumbs-up`'
                :label='String(postData.likes)'
                :loading='likeButtonLoading'
                @click='clickLikeButton'
            />
        </div>
    </div>
</template>

<style>
@import url('./ProfilePostView.css');
</style>