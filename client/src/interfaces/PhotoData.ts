import type { PostData } from "./PostData";

export interface PhotoData {
    id: string;
    post_position: number;
    image_src: string;
    image_id: string;
    post: PostData | null;
}