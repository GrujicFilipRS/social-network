import { Fetch } from "../api";
import type { ProfileData } from "../interfaces/ProfileData";

export interface EditProfileData {
    status: number;
    username: string;
    pfp_src: string;
    name: string;
}

export const GetSelfProfileForEditing = async (): Promise<EditProfileData> => {
    return await Fetch('user/get_current_user_profile/')
    .then(async res => {
        const status = res.status;
        const data: ProfileData = await res.json() as ProfileData;

        return {
            status: status,
            username: data.username,
            pfp_src: data.pfp_src ?? '/default-pfp.png',
            name: data.user_name ?? 'Set your name here'
        }
    });
}