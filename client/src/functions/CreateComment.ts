import axios from 'axios';
import { type CommentGetResponse } from '../interfaces/CommentGetResponse';

export const CreateComment = async (
    postId: string,
    commentBody: string,
    toastAdd: (message: string, severity: "success" | "error") => void,
    clearCommentInput: () => void,
    setLoading: (loading: boolean) => void,
    callback: () => void
) => {
    setLoading(true);

    axios.post('comment/post_comment', {
        body: commentBody,
        comment_id: null,
        post_id: postId
    })
    .then((res) => {
        const data = res.data as CommentGetResponse;

        if (!data.success || !data.comment) {
            setLoading(false);
            toastAdd(
                data.message ?? 'There was an error while uploading comment',
                'error'
            );
            return;
        }

        clearCommentInput();
        toastAdd('Comment posted successfully', 'success');
    })
    .catch(() => {
        toastAdd('There was an error while uploading comment', 'error');
        clearCommentInput();
    })
    .finally(() => {
        setLoading(false);
        callback();
    })
}