import { API_ROUTE } from "../api"

export const GetProfile = async (
    username: string | null
) => {
    if (!username) return GetSelfProfile();

    return fetch(`${API_ROUTE}/user/get_user_profile/?username=${username}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    }).then(async (res) => {
        return {status: res.status, data: await res.json()};
    })
}

export const GetSelfProfile = async () => {
    const token = localStorage.getItem('jwt');

    return fetch(`${API_ROUTE}/user/get_current_user_profile/`, {
        method: 'GET',
        headers: {
            'Authorization': `${token}`
        },
        credentials: 'include'
    }).then(async (res) => {
        return {status: res.status, data: await res.json()};
    })
}