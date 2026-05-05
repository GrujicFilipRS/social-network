import { Fetch } from '../api';

export const GetFollowerUsernameFromFollowId = async (followId: string): Promise<string> => {
    const response = await Fetch(`follow/get_follower_username_from_follow_id/${followId}`);

    const data = await response.json();
    return data.follower_username;
}