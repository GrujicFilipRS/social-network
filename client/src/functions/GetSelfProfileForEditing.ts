import { Fetch } from '../api';
import type { ProfileData } from '../interfaces/ProfileData';

export interface EditProfileData {
    usernameText: string;
    pfp_src: string;
    nameText: string;
}

export const GetSelfProfileForEditing = async (): Promise<EditProfileData[]> => {
    return await Fetch('user/get_current_user_profile/')
    .then(async res => {
        const data: ProfileData = await res.json() as ProfileData;

        return [{
            usernameText: data.username,
            pfp_src: data.pfp_src ?? '/default-pfp.png',
            nameText: data.user_name ?? 'Set your name here'
        }, {
            usernameText: data.username,
            pfp_src: data.pfp_src ?? '/default-pfp.png',
            nameText: data.user_name ?? ''
        }]
    });
}