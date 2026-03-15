import type { Router } from 'vue-router';
import { Fetch } from '../api';

export const DeletePost = async (
    postId: string,
    showErrorToast: (message: string) => void,
    router: Router,
    setLoading: (value: boolean) => void
) => {
    setLoading(true);

    Fetch(`post/delete_post/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postId })
    })
    .then(async res => {
        const data = await res.json();

        if (!res.ok) {
            showErrorToast(data.message);
            return;
        }

        router.push('/profile');
    })
    .then(() => setLoading(false));
}