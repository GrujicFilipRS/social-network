<script setup lang='ts'>
import { ref } from 'vue';
import type { CommentsData } from '../interfaces/CommentsData';

import Button from 'primevue/button';
import { DeleteComment } from '../functions/DeleteComment';

const props = defineProps<{
    commentData: CommentsData
    userId: string
    toastAdd: (message: string, severity: 'success' | 'error') => void
    callbackFetch: () => void
}>();

const deleteLoading = ref<boolean>(false);

const deleteComment = async () => {
    await DeleteComment(
        props.commentData.id,
        props.toastAdd,
        (loading: boolean) => deleteLoading.value = loading
    );

    props.callbackFetch();
};

</script>

<template>
    <div class='comment-header'>
        <img :src='props.commentData.creator.pfp ?? "/default-pfp.png"' class='comment-pfp' />
        <p>{{ props.commentData.creator.name ?? props.commentData.creator.username }}</p>
        <p>{{ props.commentData.commented_at }}</p>
    </div>

    <p style='white-space: pre-line;'>{{ props.commentData.body }}</p>
    
    <Button
        v-if='props.commentData.creator.id === props.userId'
        label='Delete Comment'
        icon='pi pi-trash'
        severity='danger'
        :loading='deleteLoading'
        @click='deleteComment'
    />
</template>