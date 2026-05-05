import { Fetch } from '../api';

export const GetPostIdFromCommentId = async (commentId: string): Promise<string> => {
    const response = await Fetch(`comment/get_post_id_from_comment_id/${commentId}`);

    const data = await response.json();
    return data.post_id;
}