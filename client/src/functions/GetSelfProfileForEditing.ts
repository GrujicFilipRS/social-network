import { Fetch } from "../api";
import type { ProfileData } from "../interfaces/ProfileData";

export interface EditProfileData {
    status: number;
    usernameText: string;
    pfp_src: string;
    nameText: string;
}

export const GetSelfProfileForEditing = async (): Promise<EditProfileData> => {
    return await Fetch('user/get_current_user_profile/')
    .then(async res => {
        const status = res.status;
        const data: ProfileData = await res.json() as ProfileData;

        return {
            status: status,
            usernameText: data.username,
            pfp_src: data.pfp_src ?? '/default-pfp.png',
            nameText: data.user_name ?? 'Set your name here'
        }
    });
}