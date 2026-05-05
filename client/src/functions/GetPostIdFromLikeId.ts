import { Fetch } from '../api';

export const GetPostIdFromLikeId = async (likeId: string): Promise<string> => {
    return Fetch(`post/get_post_id_from_like_id/${likeId}`)
    .then(async res => {
        if (!res.ok) {
            return '';
        }

        const data = await res.json();
        return data.post_id;
    })
    .catch((e) => {
        console.error('Error fetching post ID from like ID:', e);
        return '';
    });
}