<script lang='ts' setup>
import { ref } from 'vue';
import type { UserData } from '../interfaces/UserData';

const props = defineProps<{
    user: UserData
}>();

const pfpToShow = ref<string>(props.user.pfp || './default-pfp.png');
const linkToProfile = ref<string>(`/profile?user=${props.user.username}`);

</script>

<template>
    <div class='follow-box'>
        <img :src='pfpToShow' class='follow-pfp' />
        <a
            :href='linkToProfile'
            class='follow-profile-link'
            title='Visit profile'
        >{{ props.user.username }}</a>
    </div>
</template>

<style>
@import url('./FollowBox.css');
</style>