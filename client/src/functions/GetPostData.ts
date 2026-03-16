import type { Router } from "vue-router";
import { Fetch } from "../api";
import { type PostData } from "../interfaces/PostData";

export const GetPostData = async (
    postId: string,
    router: Router
): Promise<PostData | null> => {
    return Fetch(`post/get_post/?post_id=${postId}`)
    .then(async res => {
        const status = res.status;
        const data = await res.json();
        if (status === 200) {
            return data.post as PostData;
        }

        router.push('/feed');
        return null;
    });
}