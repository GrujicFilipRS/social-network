import axios from "axios";
import type { PhotoData } from "../interfaces/PhotoData";
import type { PhotoListResponse } from "../interfaces/PhotoListResponse";

export const GetPostPhotos = async (
    post_id: string,
    errorToast?: (_: string) => void
): Promise<PhotoData[]> => {
    return await axios.get(`photo/get_post_photos/${post_id}`)
    .then(async res => {
        const data = res.data as PhotoListResponse;

        if (data.success === false && errorToast) {
            errorToast(data.message ?? 'Error while fetching post images');
            return [];
        }

        return data.photos;
    }).catch(() => {
        if (errorToast) {
            errorToast('Error while fetching post images');
        }
        return [];
    });
}