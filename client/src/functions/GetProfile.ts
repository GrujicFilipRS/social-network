import axios from 'axios';
import type { UserProfileGetResponse } from '../interfaces/UserProfileGetResponse';
import type { Router } from 'vue-router';
import type { PostData } from '../interfaces/PostData';
import type { ProfileData } from '../interfaces/ProfileData';

/*

if (fetchData.value.status === 404) {
        router.push('/feed');
        return;
    }

    fetchData.value = {status, data};
    postData.value = fetchData.value.data!.posts!;
    profileData.value = fetchData.value.data!;

    followingUser.value = profileData.value!.user_followed;

    firstRow.value = profileData.value.user_name ? profileData.value.user_name : profileData.value.username;
    secondRow.value = profileData.value.user_name ? profileData.value.username : '';

*/

export const GetProfile = async (
    username: string | null,
    router: Router,
    setPostData: (_: PostData[]) => void,
    setProfileData: (_: ProfileData) => void,
    setFollowingUser: (_: boolean) => void,
    setFirstRow: (_: string) => void,
    setSecondRow: (_: string) => void
) => {
    if (!username) return await GetSelfProfile(
        router,
        setPostData,
        setProfileData,
        setFollowingUser,
        setFirstRow,
        setSecondRow
    );

    return axios.get(`user/get_user_profile/${username}`)
    .then(res => {
        const data: UserProfileGetResponse = res.data;

        if (!data.success || !data.user) {
            console.error(data.message ?? 'Failed to fetch user profile');
            router.push('/feed');
            return;
        }

        setPostData(data.posts);
        setProfileData({
            user_id: data.user.id,
            username: data.user.username,
            user_name: data.user.name,
            num_followers: data.num_followers,
            num_followed: data.num_follows,
            posts: data.posts,
            pfp_src: data.user.pfp_src,
            user_followed: data.user_followed
        });
        setFollowingUser(data.user_followed);
        setFirstRow(data.user.name ?? data.user.username);
        setSecondRow(data.user.name ? data.user.username : '');
    });
}

export const GetSelfProfile = async (
    router: Router,
    setPostData: (_: PostData[]) => void,
    setProfileData: (_: ProfileData) => void,
    setFollowingUser: (_: boolean) => void,
    setFirstRow: (_: string) => void,
    setSecondRow: (_: string) => void
) => {
    return axios.get(`user/get_current_user_profile`)
    .then(res => {
        const data: UserProfileGetResponse = res.data;

        if (!data.success || !data.user) {
            console.error(data.message ?? 'Failed to fetch user profile');
            router.push('/feed');
            return;
        }

        setPostData(data.posts);
        setProfileData({
            user_id: data.user.id,
            username: data.user.username,
            user_name: data.user.name,
            num_followers: data.num_followers,
            num_followed: data.num_follows,
            posts: data.posts,
            pfp_src: data.user.pfp_src,
            user_followed: data.user_followed
        });
        setFollowingUser(data.user_followed);
        setFirstRow(data.user.name ?? data.user.username);
        setSecondRow(data.user.name ? data.user.username : '');
    });
}