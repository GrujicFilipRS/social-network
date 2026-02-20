import { Fetch } from '../api';

export const EditComment = (
    commentId: string,
    newBody: string,
    toastAdd: (message: string, severity: 'success' | 'error') => void,
    setLoading: (val: boolean) => void,
    callbackFetch: () => void,
    closeEditForm: () => void
) => {
    setLoading(true);

    Fetch('comment/edit_comment/', {
        method: 'PUT',
        body: JSON.stringify({
            comment_id: commentId,
            body: newBody
        })
    })
    .then(async res => {
        const data = await res.json();

        if (res.status !== 200) {
            toastAdd(data.message, 'error');
            return;
        }

        toastAdd('Successfully updated comment', 'success');
    })
    .finally(() => {
        setLoading(false);
        callbackFetch();
        closeEditForm();
    });
}