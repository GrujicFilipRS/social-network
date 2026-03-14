<script setup lang='ts'>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { verifyUser } from '../api';

import { GetProfile } from '../functions/GetProfile';
import { Follow, Unfollow } from '../functions/Follow';
import { GetProfilePosts } from '../functions/GetProfilePosts';

import type { ProfileData } from '../interfaces/ProfileData';
import type { FollowWindowModeType } from '../interfaces/FollowWindowModeType';
import type { PostData } from '../interfaces/PostData';

import Button from 'primevue/button';

import FollowsWindow from '../components/FollowWindow.vue';
import ProfilePostView from '../components/ProfilePostView.vue';

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

const userId: string = verificationData.result['user']['id'];

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username: string | null = urlParams.get('user');

const fetchData = ref<{status: number, data: ProfileData}>(await GetProfile(username) as {status: number, data: ProfileData});
const postData = ref<PostData[]>(await GetProfilePosts(username ?? verificationData.result['user']['username']));

if (fetchData.value.status === 404) {
    router.push('/feed');
}

const data = ref<ProfileData>(fetchData.value.data);

const firstRow: string = data.value.user_name ? data.value.user_name : data.value.username;
const secondRow: string | null = data.value.user_name ? data.value.username : null;

const followingUser = ref<boolean>(data.value.user_followed);
const followWindowRef = ref<InstanceType<typeof FollowsWindow>>();

const handleFollow = async () => { Follow(data.value.user_id, followingUser); };
const handleUnfollow = async () => { Unfollow(data.value.user_id, followingUser); };
const handleEdit = async () => { router.push('/edit_profile'); };
const showFollows = (mode: FollowWindowModeType) => { followWindowRef.value!.showWindow(mode); };

</script>

<template>
    <div class='profile-info'>
        <div class='lside-info'>
            <div class='pfp'>
                <img :src='data.pfp_src ?? "/default-pfp.png"' />
            </div>

            <div class='names'>
                <h2>{{ firstRow }}</h2>
                <p>{{ secondRow }}</p>
            </div>
        </div>

        <div class='rside-info'>
            <div class='follows'>
                <p>
                    Following:
                    <span
                        class='bold'
                        title='See follows'
                        @click='() => {showFollows("FOLLOWING")}'
                    >
                        {{ data.num_followed }}
                    </span>
                </p>

                <p>
                    Followers:
                    <span
                        class='bold'
                        title='See followers'
                        @click='() => {showFollows("FOLLOWERS")}'
                    >
                        {{ data.num_followers }}
                    </span>
                </p>
            </div>

            <Button
                v-show='userId !== data.user_id && !followingUser'
                @click='handleFollow'
                label='FOLLOW'
                class='follow-button'
            />

            <Button
                v-show='userId !== data.user_id && followingUser'
                @click='handleUnfollow'
                label='Unfollow'
                severity='secondary'
            />

            <Button
                v-show='userId == data.user_id'
                @click='handleEdit'
                label='Edit profile'
                severity='secondary'
                icon='pi pi-pencil'
            />
        </div>
    </div>

    <div class='w-[60%] mt-6'>
        <Button
            v-if='userId == data.user_id'
            label='Create new post'
            severity='secondary'
            class='self-start'
            @click='() => router.push("/create_post")'
            icon='pi pi-plus'
        />

        <div class='post-list'>
            <ProfilePostView :postData='post' :key='post.id' v-for='post in postData' />
        </div>
    </div>

    <FollowsWindow
        ref='followWindowRef'
        :userId='data.user_id'
    />
</template>

<style>
@import url('./Profile.css');
</style>