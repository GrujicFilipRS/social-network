import { Fetch } from '../api';

export const CreateComment = async (
    postId: string,
    commentBody: string,
    toastAdd: (message: string, severity: "success" | "error") => void,
    clearCommentInput: () => void,
    setLoading: (loading: boolean) => void,
    callback: () => void
) => {
    setLoading(true);

    Fetch('comment/post_comment/', {
        method: 'POST',
        body: JSON.stringify({
            post_id: postId,
            body: commentBody
        })
    }).then(async res => {
        const status = res.status;
        const data = await res.json();
        if (status !== 201) {
            toastAdd(data.message ?? 'Failed to post comment', 'error');
            return;
        }

        clearCommentInput();
        toastAdd('Comment posted successfully', 'success');
    })
    .finally(() => {
        setLoading(false);
        callback();
    });
}