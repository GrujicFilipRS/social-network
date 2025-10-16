<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { verifyUser } from '../api';

import { GetProfile } from '../functions/GetProfile';
import { CheckIfFollowing } from '../functions/CheckIfFollowing';
import { Follow, Unfollow } from '../functions/Follow';

import type { ProfileData } from '../interfaces/ProfileData';

const router = useRouter();

const userId = await verifyUser();
if (userId === -1) {
    router.push('/join');
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username: string | null = urlParams.get("user");

const data = ref<ProfileData>(await GetProfile(username) as ProfileData);

const firstRow: string = data.value.user_name ? data.value.user_name : data.value.username;
const secondRow: string | null= data.value.user_name ? data.value.username : null;

const followingUser = ref<boolean>(await CheckIfFollowing(data.value.user_id));

const handleFollow = async () => { Follow(data.value.user_id, followingUser) };
const handleUnfollow = async () => { Unfollow(data.value.user_id, followingUser) };
const handleEdit = async () => { router.push('/edit_profile'); }

</script>

<template>
    <div class="profile-info">
        <div class="lside-info">
            <div class="pfp">
                <img :src="data.pfp_src || '/default-pfp.png'" />
            </div>

            <div class="names">
                <h2>{{ firstRow }}</h2>
                <p>{{ secondRow }}</p>
            </div>
        </div>

        <div class="rside-info">
            <div class="follows">
                <p>
                    Followers:
                    <span class="bold">
                        {{ data.num_followers }}
                    </span>
                </p>

                <p>
                    Following:
                    <span class="bold">
                        {{ data.num_followed }}
                    </span>
                </p>
            </div>

            <button
                class="primary-btn"
                v-show="userId !== data.user_id && !followingUser"
                @click="handleFollow"
            >
                FOLLOW
            </button>

            <button
                class="secondary-btn"
                v-show="userId !== data.user_id && followingUser"
                @click="handleUnfollow"
            >
                Unfollow
            </button>

            <button
                class="secondary-btn"
                v-show="userId == data.user_id"
                @click="handleEdit"
            >
                Edit profile
            </button>
        </div>
    </div>

    <div class="posts">
        
    </div>
</template>

<style>
@import url('./Profile.css');
</style>