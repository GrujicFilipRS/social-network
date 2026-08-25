import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const LikePost = async (
    postId: string,
    errorToast: (message: string) => void,
    setLiked: (liked: boolean) => void,
    incrementLikes?: (_: number) => void
): Promise<boolean> => {
    // Optimistic loading
    setLiked(true);
    if (incrementLikes) incrementLikes(1);

    return axios.post(`like/like_post/${postId}`)
    .then(async res => {
        const data: DTO = res.data;

        if (!data.success) {
            if (incrementLikes)
                incrementLikes(-1);
            setLiked(false);
            errorToast(data.message ?? 'An error occured while liking post. Please try again later');
            return false;
        }

        return true;
    })
    .catch(() => {
        errorToast('An error occured while liking post. Please try again later');
        return false;
    });
}

export const UnlikePost = async (
    postId: string,
    toastAdd: (message: string) => void,
    setLiked: (liked: boolean) => void,
    setLoading: (loading: boolean) => void,
    decrementLikes?: () => void
): Promise<boolean> => {
    setLoading(true);

    return Fetch(`like/unlike_post/`, {
        method: 'DELETE',
        body: JSON.stringify({ post_id: postId })
    })
    .then(async res => {
        if (res.status !== 200) {
            const data = await res.json();
            toastAdd(data.message);
            return false;
        }

        setLiked(false);
        if (decrementLikes) decrementLikes();
        return true;
    })
    .finally(() => setLoading(false));
}