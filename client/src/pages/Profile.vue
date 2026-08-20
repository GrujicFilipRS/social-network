<script setup lang='ts'>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { verifyUser } from '../api';

import { GetProfile } from '../functions/GetProfile';
import { Follow, Unfollow } from '../functions/Follow';

import type { ProfileData } from '../interfaces/ProfileData';
import type { FollowWindowModeType } from '../interfaces/FollowWindowModeType';
import type { PostData } from '../interfaces/PostData';

import Button from 'primevue/button';

import FollowsWindow from '../components/FollowWindow.vue';
import ProfilePostView from '../components/ProfilePostView.vue';

const route = useRoute();
const router = useRouter();

let userId: string = '';

try {
    userId = (await verifyUser()).id;
} catch { router.push('/') }

const postData = ref<PostData[]>([]);
const profileData = ref<ProfileData>();

const firstRow = ref<string>('');
const secondRow = ref<string>('');

const followingUser = ref<boolean>();

const loadProfile = async () => {
    await GetProfile(
        route.query.user ? route.query.user as string : null,
        router,
        (_) => postData.value = _,
        (_) => profileData.value = _,
        (_) => followingUser.value = _,
        (_) => firstRow.value = _,
        (_) => secondRow.value = _,
    );
}

loadProfile();

const followWindowRef = ref<InstanceType<typeof FollowsWindow>>();

const handleFollow = async () => { Follow(profileData.value!.user_id, (val) => followingUser.value = val); };
const handleUnfollow = async () => { Unfollow(profileData.value!.user_id, (val) => followingUser.value = val); };
const handleEdit = async () => { router.push('/edit_profile'); };
const showFollows = (mode: FollowWindowModeType) => { followWindowRef.value!.showWindow(mode); };

watch(
    () => route.query.user,
    () => {
        loadProfile();
    }
);

</script>

<template>
    <div class='profile-info'>
        <div class='lside-info'>
            <div class='pfp'>
                <img :src='profileData?.pfp_src ?? "/default-pfp.png"' />
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
                        {{ profileData?.num_followed }}
                    </span>
                </p>

                <p>
                    Followers:
                    <span
                        class='bold'
                        title='See followers'
                        @click='() => {showFollows("FOLLOWERS")}'
                    >
                        {{ profileData?.num_followers }}
                    </span>
                </p>
            </div>

            <Button
                v-show='userId !== profileData?.user_id && !followingUser'
                @click='handleFollow'
                label='FOLLOW'
                class='follow-button'
            />

            <Button
                v-show='userId !== profileData?.user_id && followingUser'
                @click='handleUnfollow'
                label='Unfollow'
                severity='secondary'
            />

            <Button
                v-show='userId == profileData?.user_id'
                @click='handleEdit'
                label='Edit profile'
                severity='secondary'
                icon='pi pi-pencil'
            />
        </div>
    </div>

    <div class='w-[60%] mt-6'>
        <Button
            v-if='userId == profileData?.user_id'
            label='Create new post'
            severity='secondary'
            class='self-start'
            @click='() => router.push("/create_post")'
            icon='pi pi-plus'
        />

        <div class='post-list'>
            <h1 class='mt-16 text-4xl font-bold'>Newest posts</h1>

            <ProfilePostView
                :router='router'
                :postData='post'
                :key='post.id'
                v-for='post in postData'
            />
        </div>
    </div>

    <FollowsWindow
        ref='followWindowRef'
        :userId='profileData?.user_id'
    />
</template>

<style>
@import url('./Profile.css');
</style>