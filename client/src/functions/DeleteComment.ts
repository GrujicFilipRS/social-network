import { Fetch } from '../api';

export const DeleteComment = (
    commentId: string,
    toastAdd: (message: string, severity: 'success' | 'error') => void,
    setLoading: (loading: boolean) => void,
    callbackFetch: () => void
) => {
    setLoading(true);

    Fetch('comment/remove_comment/', {
        method: 'DELETE',
        body: JSON.stringify({ comment_id: commentId })
    })
    .then(async res => {
        const statusCode = res.status;
        const data = await res.json();

        if (statusCode !== 200) {
            toastAdd(data.message || 'Failed to delete comment', 'error');
            return;
        }

        toastAdd('Comment deleted successfully', 'success');
    })
    .finally(() => {
        setLoading(false);
        callbackFetch();
    });
}