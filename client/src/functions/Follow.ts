import type { Ref } from "vue";
import { Fetch } from "../api"

export const Follow = async (
    userId: string,
    followedRef: Ref<boolean>
) => {
    return Fetch('follow/follow_user/', {
        method: 'POST',
        body: JSON.stringify({ to_follow_id: userId })
    }).then(async (res) => {
        followedRef.value = true;
        return res;
    })
}

export const Unfollow = async (
    userId: string,
    followedRef: Ref<boolean>
) => {
    return Fetch('follow/unfollow_user/', {
        method: 'DELETE',
        body: JSON.stringify({ to_unfollow_id: userId })
    }).then(async (res) => {
        followedRef.value = false;
        return res;
    })
}