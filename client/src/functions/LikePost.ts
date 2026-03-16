import { Fetch } from '../api';

export const LikePost = async (
    postId: string,
    toastAdd: (message: string) => void,
    setLiked: (liked: boolean) => void,
    setLoading: (loading: boolean) => void,
    incrementLikes?: () => void
): Promise<boolean> => {
    setLoading(true);

    return Fetch(`like/like_post/`, {
        method: 'POST',
        body: JSON.stringify({ post_id: postId })
    })
    .then(async res => {
        if (res.status !== 201) {
            const data = await res.json();
            toastAdd(data.message);
            return false;
        }

        setLiked(true);
        if (incrementLikes) incrementLikes()
        return true;
    })
    .finally(() => setLoading(false));
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