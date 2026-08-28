import type { CommentListResponse } from "../interfaces/CommentListResponse";
import type { CommentsData } from "../interfaces/CommentsData";

import axios from 'axios';

export const GetPostComments = async (
    postId: string,
    errorToast?: (_: string) => void
): Promise<CommentsData[]> => {
    return axios.get(`comment/get_post_comments/${postId}`)
    .then(async res => {
        const data = res.data as CommentListResponse;

        if (!data.success) {
            if (errorToast)
                errorToast(data.message ?? 'Something went wrong with loading post comments');
            
            return [];
        }

        return data.comments;
    })
    .catch(() => {
        if (errorToast)
            errorToast('Something went wrong with loading post comments');

        return [];
    });
}