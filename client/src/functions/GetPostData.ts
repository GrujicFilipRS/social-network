import { Fetch } from "../api";

interface PhotoData {
    id: string;
    post_position: number;
    image_src: string;
    image_id: string;
}

export interface PostData {
    id: string;
    title: string;
    body: string;
    status: 'PUBLIC' | 'PRIVATE';
    created_at: string;
    user_id: string;
    photos: PhotoData[];
}

export const GetPostData = async (postId: string): Promise<PostData | null> => {
    return Fetch(`post/get_post/?post_id=${postId}`)
    .then(async res => {
        const status = res.status;
        const data = await res.json();
        if (status === 200) {
            return data.post as PostData;
        }

        return null;
    });
}