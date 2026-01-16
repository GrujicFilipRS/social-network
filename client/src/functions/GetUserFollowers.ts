import { Fetch } from "../api"
import type { FollowsData } from "../interfaces/FollowData";

export const GetUserFollowers = async (userId: string) => {
    return Fetch(`follow/get_user_followers/?user_id=${userId}`)
    .then(async (res) => {
        if (!res.ok) return res;

        return (await res.json() as FollowsData);
    })
}