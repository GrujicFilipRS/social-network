<script setup lang='ts'>
import { ref } from 'vue';
import type { CommentsData } from '../interfaces/CommentsData';

import { DeleteComment } from '../functions/DeleteComment';
import { EditComment } from '../functions/EditComment';

import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import ConfirmPopup from 'primevue/confirmpopup';
import { useConfirm } from 'primevue/useconfirm';

const props = defineProps<{
    commentData: CommentsData
    userId: string
    toastAdd: (message: string, severity: 'success' | 'error') => void
    callbackFetch: () => void
}>();

const deleteLoading = ref<boolean>(false);
const editLoading = ref<boolean>(false);
const beingEdited = ref<boolean>(false);
const commentEditingText = ref<string>(props.commentData.body);

const confirm = useConfirm();

const confirmDelete = () => {
    confirm.require({
        message: 'Are you sure you want to delete this comment?',
        header: 'Confirm Deletion',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Yes, Delete',
        rejectLabel: 'No, Keep',
        rejectProps: { severity: 'secondary' },
        acceptClass: 'p-button-danger',
        accept: deleteComment
    });
};

const closeEditForm = () => {
    beingEdited.value = false;
    commentEditingText.value = props.commentData.body;
}

const deleteComment = async () => {
    await DeleteComment(
        props.commentData.id,
        props.toastAdd,
        (loading: boolean) => deleteLoading.value = loading,
        props.callbackFetch
    );
};

const editComment = async () => {
    EditComment(
        props.commentData.id,
        commentEditingText.value,
        props.toastAdd,
        (loading: boolean) => editLoading.value = loading,
        props.callbackFetch,
        closeEditForm
    );

    props.callbackFetch();
}

</script>

<template>
    <ConfirmPopup />
    <div class='comment-header'>
        <img :src='props.commentData.creator.pfp ?? "/default-pfp.png"' class='comment-pfp' />
        <p>{{ props.commentData.creator.name ?? props.commentData.creator.username }}</p>
        <p>{{ props.commentData.commented_at }}</p>
    </div>

    <p style='white-space: pre-line;' v-if='!beingEdited'>{{ props.commentData.body }}</p>

    <div
        v-if='beingEdited'
        class='comment-edit'
    >
        <Textarea
            v-model='commentEditingText'
            style='resize: none'
        />

        <Button
            icon='pi pi-check'
            :loading='editLoading'
            @click='editComment'
        />

        <Button
            icon='pi pi-times'
            severity='danger'
            @click='closeEditForm'
        />
    </div>
    
    <div v-if='props.commentData.creator.id === props.userId'>
        <Button
            :disabled='beingEdited'
            icon='pi pi-pencil'
            severity='secondary'
            style='font-size: 0.7rem'
            @click='beingEdited = true'
        />
        
        <Button
            icon='pi pi-trash'
            severity='danger'
            style='font-size: 0.7rem'
            :loading='deleteLoading'
            @click='confirmDelete'
        />
    </div>
    
</template>