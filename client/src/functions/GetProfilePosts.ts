import { Fetch } from '../api';
import type { PostData } from '../interfaces/PostData';

export const GetProfilePosts = async (username: string): Promise<PostData[]> => {
    return Fetch(`post/get_profile_posts/?username=${username}`)
    .then(async res => {
        const data = await res.json();

        return data.posts;
    });
}