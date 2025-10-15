import { API_ROUTE } from "../api";

export const CheckIfFollowing = async (userId: number) => {
    const token = localStorage.getItem('jwt');

    return fetch(
        `${API_ROUTE}/follow/check_if_following/?user_id=${userId}`,
        {
            method: 'GET',
            headers: {
                'Authorization': `${token}`,
                'Content-Type': 'application/json'
            }
        }
    ).then(async (res) => {
        const data = (await res.json()) as { following: boolean };
        return data.following;
    })
}