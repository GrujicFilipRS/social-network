import { API_ROUTE } from "../api"

export const GetProfile = async (
    username: string | null
) => {
    if (!username) return GetSelfProfile();

    return fetch(`${API_ROUTE}/user/get_user_profile/?username=${username}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(async (res) => {
        return (res.status, await res.json());
    })
}

const GetSelfProfile = async () => {
    const token = localStorage.getItem('jwt');

    return fetch(`${API_ROUTE}/user/get_current_user_profile/`, {
        method: 'GET',
        headers: {
            'Authorization': `${token}`,
            'Content-Type': 'application/json'
        }
    }).then(async (res) => {
        return (res.status, await res.json());
    })
}