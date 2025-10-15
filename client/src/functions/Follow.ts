import type { Ref } from "vue";
import { API_ROUTE } from "../api"

export const Follow = async (
    userId: number,
    followedRef: Ref<boolean>
) => {
    const token = localStorage.getItem('jwt');

    return fetch(`${API_ROUTE}/follow/follow_user/`, {
        method: 'POST',
        body: JSON.stringify({ to_follow_id: userId }),
        headers: {
            'Authorization': `${token}`,
            'Content-Type': 'application/json'
        }
    }).then(async (res) => {
        followedRef.value = true;
        return res;
    })
}

export const Unfollow = async (
    userId: number,
    followedRef: Ref<boolean>
) => {
    const token = localStorage.getItem('jwt');

    return fetch(`${API_ROUTE}/follow/unfollow_user/`, {
        method: 'DELETE',
        body: JSON.stringify({ to_follow_id: userId }),
        headers: {
            'Authorization': `${token}`,
            'Content-Type': 'application/json'
        }
    }).then(async (res) => {
        followedRef.value = false;
        return res;
    })
}