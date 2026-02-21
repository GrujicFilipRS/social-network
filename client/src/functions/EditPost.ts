import { Fetch } from '../api'

export const EditPost = (
    postId: string,
    newTitle: string,
    newBody: string,
    newStatus: 'PRIVATE' | 'PUBLIC',
    toastAdd: (message: string, severity: 'error' | 'success') => void,
    closeEditForm: () => void,
    setLoading: (loading: boolean) => void,
    callback: () => void
) => {
    setLoading(true);
    
    Fetch('post/edit_post/', {
        method: 'PUT',
        body: JSON.stringify({
            id: postId,
            title: newTitle,
            body: newBody,
            status: newStatus
        })
    })
    .then(async res => {
        const data = await res.json();

        if (res.status !== 200) {
            toastAdd(data.message, 'error');
            return;
        }

        toastAdd('Successfully edited post', 'success');
    })
    .finally(() => {
        closeEditForm();
        callback();
        setLoading(false);
    });
}