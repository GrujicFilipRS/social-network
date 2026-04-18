import { Fetch } from '../api'

export const Follow = async (
    userId: string,
    setFollowedRef: (val: boolean) => void
) => {
    return Fetch('follow/follow_user/', {
        method: 'POST',
        body: JSON.stringify({ to_follow_id: userId })
    }).then(async (res) => {
        setFollowedRef(true);
        return res;
    })
}

export const Unfollow = async (
    userId: string,
    setFollowedRef: (val: boolean) => void
) => {
    return Fetch('follow/unfollow_user/', {
        method: 'DELETE',
        body: JSON.stringify({ to_unfollow_id: userId })
    }).then(async (res) => {
        setFollowedRef(false);
        return res;
    })
}