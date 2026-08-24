import axios from "axios";
import type { PostMiscResponse } from "../interfaces/PostMiscResponse";

export const GetPostMiscData = async (post_id: string): Promise<PostMiscResponse> => {
    return await axios.get(`post/misc_data/${post_id}`)
    .then(async res => {
        const data = await res.data as PostMiscResponse;
        return data;
    });
}