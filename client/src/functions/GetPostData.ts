import { type PostData } from "../interfaces/PostData";
import type { PostGetResponse } from "../interfaces/PostGetResponse";

import axios from 'axios';

export const GetPostData = async (
    postId: string
): Promise<PostData | null> => {
    return axios.get(`post/get_post/${postId}`)
    .then(async res => {
        const data = res.data as PostGetResponse;

        return data.post;
    });
}