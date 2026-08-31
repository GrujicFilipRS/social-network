import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const DeleteComment = (
    commentId: string,
    toastAdd: (message: string, severity: 'success' | 'error') => void,
    setLoading: (loading: boolean) => void,
    callbackFetch: () => void
) => {
    setLoading(true);

    axios.delete(`comment/remove_comment/${commentId}`)
    .then((res) => {
        const data = res.data as DTO;

        if (!data.success) {
            toastAdd(data.message ?? 'Failed to delete comment', 'error');
            return;
        }

        toastAdd('Comment deleted successfully', 'success');
    })
    .catch(() => {
        toastAdd('Failed to delete comment', 'error');
    })
    .finally(() => {
        setLoading(false);
        callbackFetch();
    })
}