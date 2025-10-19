import type { PostData } from './PostData';

export interface ProfileData {
    user_id: number,
    username: string,
    user_name: string | null,
    num_followers: number,
    num_followed: number,
    posts: PostData[],
    pfp_src: string,
    user_followed: boolean
};