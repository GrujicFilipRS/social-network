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
    errorToast: (message: string) => void,
    setLiked: (liked: boolean) => void,
    decrementLikes?: (_: number) => void
): Promise<boolean> => {
    setLiked(false);
    if (decrementLikes) decrementLikes(1);

    return axios.delete(`like/unlike_post/${postId}`)
    .then(async res => {
        const data: DTO = res.data;

        if (!data.success) {
            if (decrementLikes)
                decrementLikes(-1);
            setLiked(true);
            errorToast(data.message ?? 'An error occured while unliking post. Please try again later');
            return false;
        }

        return true;
    })
    .catch(() => {
        if (decrementLikes)
            decrementLikes(-1);
        setLiked(true);
        errorToast('An error occured while unliking post. Please try again later');
        return false;
    });
}