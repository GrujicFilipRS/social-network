<script lang='tsx' setup>
import { nextTick, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import Comment from '../components/Comment.vue';

import { UserUnverifiedError, verifyUser } from '../api';
import { GetPostData } from '../functions/GetPostData';
import { LikePost, UnlikePost } from '../functions/LikePost';
import { CreateComment } from '../functions/CreateComment';
import { EditPost } from '../functions/EditPost';
import { DeletePost } from '../functions/DeletePost';
import { type PhotoData } from '../interfaces/PhotoData';
import { GetPostPhotos } from '../functions/GetPostPhotos';
import { type PostMiscResponse } from '../interfaces/PostMiscResponse';
import type { PostData } from '../interfaces/PostData';
import { GetPostMiscData } from '../functions/GetPostMiscData';
import { type CommentsData } from '../interfaces/CommentsData';
import { GetPostComments } from '../functions/GetPostComments';

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Select from 'primevue/select';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import ConfirmPopup from 'primevue/confirmpopup';
import { useConfirm } from 'primevue/useconfirm';

const router = useRouter();

const currentUserId = ref<string>('');

await verifyUser()
    .then((user) => currentUserId.value = user.id)
    .catch((_: UserUnverifiedError) => router.push('/'));

const route = useRoute();

const postId: string | null = route.params.post_id ? String(route.params.post_id) : null;

if (!postId || typeof postId !== 'string') {
    router.push('/feed');
}

const toast = useToast();
const confirm = useConfirm();

const postData = ref<PostData | null>(null);
const likeLoading = ref<boolean>(false);
const commentInput = ref<string>('');
const commentedLoading = ref<boolean>(false);
const photos = ref<PhotoData[]>([]);
const postMiscData = ref<PostMiscResponse | null>(null);
const comments = ref<CommentsData[]>([]);

const editingPost = ref<boolean>(false);
const editLoading = ref<boolean>(false);
const editedTitle = ref<string>('');
const editedBody = ref<string>('');
const editedStatus = ref<'PUBLIC' | 'PRIVATE'>('PUBLIC');
const deleteLoading = ref<boolean>(false);

const scrollToComment = async () => {
    await nextTick();

    const hash = window.location.hash;

    if (!hash) return;

    const element = document.querySelector(hash);

    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
};

const resetEditingForm = () => {
    editedTitle.value = postData.value!.title;
    editedBody.value = postData.value!.body;
    editedStatus.value = postData.value!.status;
    editingPost.value = false;
}

const submitEdit = () => {
    EditPost(
        postData.value!.id,
        editedTitle.value,
        editedBody.value,
        editedStatus.value,
        (message: string, severity: string) => toast.add({
            severity: severity,
            summary: message,
            life: 3000
        }),
        resetEditingForm,
        (loading: boolean) => editLoading.value = loading,
        fetchPostData
    );
}

const confirmEdit = () => {
    confirm.require({
        message: 'Are you sure you want to edit this post?',
        header: 'Confirm Edit',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Yes, Edit',
        rejectLabel: 'No',
        rejectProps: { severity: 'secondary' },
        acceptClass: 'p-button-success',
        acceptIcon: 'pi pi-check',
        rejectIcon: 'pi pi-times',
        accept: submitEdit
    });
}

const fetchPostData = async () => {
    if (!postId) {
        router.push('/feed');
        return;
    }

    postData.value = await GetPostData(postId);
    resetEditingForm();

    if (postData.value === null) {
        router.push('/feed');
        return;
    }

    photos.value = await GetPostPhotos(postId);
    postMiscData.value = await GetPostMiscData(postId);
    comments.value = await GetPostComments(postId);

    await scrollToComment();
};

fetchPostData();

const deletePost = () => {
    DeletePost(
        postId!,
        (message: string) => toast.add({
            summary: 'Error while deleting post',
            detail: message,
            life: 3000,
            severity: 'error'
        }),
        router,
        (val: boolean) => deleteLoading.value = val
    )
}

const showPostDeleteConfirmPopup = () => {
    confirm.require({
        message: 'Are you sure you want to delete this post?',
        header: 'Confirm Delete',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Yes, Delete',
        rejectLabel: 'No',
        rejectProps: { severity: 'secondary' },
        acceptClass: 'p-button-danger',
        acceptIcon: 'pi pi-trash',
        rejectIcon: 'pi pi-times',
        accept: deletePost
    });
}

const pressLikeButton = async () => {
    if (!postData.value || !postId || !postMiscData.value) return;

    if (!postMiscData.value.liked_by_user) {
        await LikePost(
            postId,
            (message: string) => toast.add({
                severity: "error",
                summary: message,
                life: 3000
            }),
            (value: boolean) => postMiscData.value!.liked_by_user = value,
            (value: number) => postMiscData.value!.num_likes += value
        );
    } else {
        await UnlikePost(
            postData!.value.id,
            (message: string) => toast.add({
                severity: "error",
                summary: message,
                life: 3000
            }),
            (value: boolean) => postMiscData.value!.liked_by_user = value,
            (value: number) => postMiscData.value!.num_likes -= value
        );
    }
}

const postComment = async () => {
    if (!postId) return;
    if (!commentInput.value.trim()) return;

    CreateComment(
        postId,
        commentInput.value.trim(),
        (message: string, severity: "success" | "error") => toast.add({
            severity: severity,
            summary: message,
            life: 3000
        }),
        () => commentInput.value = '',
        (loading: boolean) => commentedLoading.value = loading,
        fetchPostData
    );
};

</script>

<template>
    <Toast />
    <ConfirmPopup />
    <div class='user-header'>
        <div class='lside-user'>
            <img :src='postData?.user.pfp_src ?? "/default-pfp.png"' class='pfp' />
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
            <p v-if='postData?.status === "PRIVATE"'>Private Post</p>

            <Button
                v-if='currentUserId === postData?.user.id'
                severity='secondary'
                class='p-button-sm'
                icon='pi pi-pencil'
                label='Edit post'
                :disabled='editingPost'
                :loading='editLoading'
                @click='editingPost = true'
            />

            <Button
                v-if='currentUserId === postData?.user.id'
                severity='danger'
                class='p-button-sm'
                icon='pi pi-trash'
                label='Delete post'
                @click='showPostDeleteConfirmPopup'
                :loading='deleteLoading'
            />
        </div>
    </div>

    <div class='post'>
        <h2
            v-if='!editingPost'
            class='text-4xl font-bold'
        >
            {{ postData?.title }}
        </h2>

        <p
            v-if='!editingPost'
            style='white-space: pre-line;'
        >
            {{ postData?.body }}
        </p>

        <InputText
            v-if='editingPost'
            v-model='editedTitle'
        />

        <Textarea
            v-if='editingPost'
            v-model='editedBody'
            style='resize: none'
        />

        <Select
            v-if='editingPost'
            v-model='editedStatus'
            :options='["PUBLIC", "PRIVATE"]'
        />

        <Button
            v-if='editingPost'
            icon='pi pi-check'
            @click='confirmEdit'
        />

        <Button
            v-if='editingPost'
            icon='pi pi-times'
            severity='danger'
            @click='resetEditingForm'
        />

        <div class='image-list'>
            <img
                v-for='image in photos'
                :key='image.post_position'
                :src='image.image_src'
                class='post-image'
            />
        </div>

        <div class='flex items-center gap-2 mt-4'>
            <Button
                :icon='postMiscData?.liked_by_user ? "pi pi-thumbs-up-fill" : "pi pi-thumbs-up"'
                severity='secondary'
                :loading='likeLoading'
                @click='pressLikeButton'
            />

            <p>{{ postMiscData?.num_likes }}</p>
        </div>

        <div class='comments'>
            <h3 class='text-2xl font-bold'>Comments</h3>

            <Comment
                v-for='comment in comments'
                :key='comment.id'
                :comment-data='comment'
                :user-id='currentUserId'
                :callback-fetch='fetchPostData'
                :toast-add='
                (message: string, severity: "success" | "error") => toast.add(
                    {severity, summary: message, life: 3000}
                )'
            />

            <p v-if='comments.length === 0'>No comments yet</p>
            
            <div class='comment-form'>
                <h3>Write a comment</h3>

                <Textarea
                    class='w-100'
                    v-model='commentInput'
                    placeholder='Your comment here...'
                    style='resize: none;'

                />

                <Button
                    label='Post Comment'
                    severity='secondary'
                    icon='pi pi-send'
                    :disabled='!commentInput.trim()'
                    @click='postComment'
                />
            </div>
        </div>
    </div>
</template>

<style>
@import url('./ViewPost.css');
</style>