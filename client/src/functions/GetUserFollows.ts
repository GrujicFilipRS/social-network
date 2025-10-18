import { API_ROUTE } from "../api"
import type { FollowsData } from "../interfaces/FollowData";

export const GetUserFollows = async (userId: number) => {
    return fetch(`${API_ROUTE}/follow/get_user_follows/?user_id=${userId}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
    .then(async (res) => {
        if (!res.ok) return res;

        return (await res.json() as FollowsData);
    })
}