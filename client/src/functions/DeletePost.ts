import type { Router } from 'vue-router';
import type { DTO } from '../interfaces/DTO';

import axios from 'axios';

export const DeletePost = async (
    postId: string,
    showErrorToast: (message: string) => void,
    router: Router,
    setLoading: (value: boolean) => void
) => {
    setLoading(true);

    axios.delete(`post/delete_post/${postId}`)
    .then((res) => {
        const data = res.data as DTO;

        if (!data.success) {
            showErrorToast(data.message ?? 'Failed to delete post');
            return;
        }

        router.push('/profile');
    })
    .catch(() => {
        showErrorToast('Failed to delete post');
    })
    .finally(() => setLoading(false));
}