<script lang='tsx' setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { verifyUser } from '../api';
import { GetPostData } from '../functions/GetPostData';

import type { PostData } from '../interfaces/PostData';

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

    console.log(postData.value);
};

fetchPostData();

</script>

<template>
    <div class='user'>
        <img :src='postData?.user.pfp ?? "/default-pfp.png"' class='pfp' />
        <p class='text-3xl'>{{ postData?.user.name ?? postData?.user.username }}</p>
        <p>{{ postData?.user.name ? postData?.user.username : '' }}</p>
    </div>

    <div class='post'>

    </div>
</template>