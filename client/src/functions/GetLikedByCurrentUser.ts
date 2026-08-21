import axios from "axios";
import type { ExistsGetResponse } from "../interfaces/ExistsGetResponse";

export const GetLikedByCurrentUser = async (postId: string): Promise<boolean> => {
    return await axios.get(`post/liked_by_current_user/${postId}`)
    .then(async res => {
        const data = res.data as ExistsGetResponse;

        return data.exists;
    });
}