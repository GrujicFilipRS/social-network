import { Fetch } from "../api";
import { type PostData } from "../interfaces/PostData";

export const GetPostData = async (postId: string): Promise<PostData | null> => {
    return Fetch(`post/get_post/?post_id=${postId}`)
    .then(async res => {
        const status = res.status;
        const data = await res.json();
        if (status === 200) {
            return data.post as PostData;
        }

        return null;
    });
}