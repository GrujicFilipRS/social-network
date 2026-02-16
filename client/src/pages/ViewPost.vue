<script lang='tsx' setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import { GetPostData } from '../functions/GetPostData';

import type { PostData } from '../interfaces/PostData';

import Button from 'primevue/button';

const router = useRouter();

verifyUser().then(async (res) => {
    if (res.statusCode !== 200) {
        window.location.href = '/join';
    }
}).catch(() => {
    window.location.href = '/join';
});

const urlParams = new URLSearchParams(window.location.search);
const postId = urlParams.get('post_id');

if (!postId) {
    router.push('/feed');
}

const postData = ref<PostData | null>(null);

const fetchPostData = async () => {
    const data = await GetPostData(postId!);
    postData.value = data;

    if (postData.value === null) {
        router.push('/feed');
    }
};

fetchPostData();

</script>

<template>
    <div class='user-header'>
        <div class='lside-user'>
            <img :src='postData?.user.pfp ?? "/default-pfp.png"' class='pfp' />
            <p class='text-3xl'>{{ postData?.user.name ?? postData?.user.username }}</p>
            <p>{{ postData?.user.name ? postData?.user.username : '' }}</p>
        </div>

        <div class='rside-user'>
            <Button
                label='View Profile'
                class='p-button-outlined p-button-sm'
                @click='() => router.push(`/profile?user=${postData?.user.username}`)'
            />

            <p>{{ postData?.created_at }}</p>
        </div>
    </div>

    <div class='post'>
        <h2 class='text-4xl font-bold'>{{ postData?.title }}</h2>
        <p>{{ postData?.body }}</p>

        <div class='image-list'>
            <img
                v-for='image in postData?.photos ?? []'
                :key='image.post_position'
                :src='image.image_src'
                class='post-image'
            />
        </div>

        <div class='flex items-center gap-2 mt-4'>
            <Button
                icon='pi pi-thumbs-up'
                severity='secondary'
            />

            <p>{{ postData?.likes }}</p>
        </div>

        <div class='comments'>
            <h3 class='text-2xl font-bold'>Comments</h3>

            <div
                v-for='comment in postData?.comments ?? []'
                :key='comment.id'
                class='comment'
            >
                <div class='comment-header'>
                    <img :src='comment.creator.pfp ?? "/default-pfp.png"' class='comment-pfp' />
                    <p>{{ comment.creator.name ?? comment.creator.username }}</p>
                    <p>{{ comment.commented_at }}</p>
                </div>

                <p>{{ comment.body }}</p>
            </div>

            <p v-if='postData?.comments.length === 0'>No comments</p>
        </div>
    </div>
</template>

<style>
@import url('./ViewPost.css');
</style>