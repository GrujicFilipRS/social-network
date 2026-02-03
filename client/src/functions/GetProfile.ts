import { Fetch } from '../api'

export const GetProfile = async (
    username: string | null
) => {
    if (!username) return GetSelfProfile();

    return Fetch(`user/get_user_profile/?username=${username}`)
    .then(async (res) => {
        return {status: res.status, data: await res.json()};
    })
}

export const GetSelfProfile = async () => {
    return Fetch(`user/get_current_user_profile/`)
    .then(async (res) => {
        return {status: res.status, data: await res.json()};
    })
}