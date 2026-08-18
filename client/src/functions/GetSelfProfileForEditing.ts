import axios from 'axios';
import type { UserProfileGetResponse } from '../interfaces/UserProfileGetResponse';

export interface EditProfileData {
    usernameText: string;
    pfp_src: string;
    nameText: string;
}

export const GetSelfProfileForEditing = async (): Promise<EditProfileData[]> => {
    return await axios.get('user/get_current_user_profile/')
    .then(async res => {
        const data: UserProfileGetResponse = res.data as UserProfileGetResponse;

        if (!data.success || data.user === null) {
            // TODO: add error toast
            return [{
                usernameText: '',
                pfp_src: '/default-pfp.png',
                nameText: ''
            }];
        }

        return [{
            usernameText: data.user.username,
            pfp_src: data.user.pfp_src ?? '/default-pfp.png',
            nameText: data.user.name ?? 'Set your name here'
        }, {
            usernameText: data.user.username,
            pfp_src: data.user.pfp_src ?? '/default-pfp.png',
            nameText: data.user.name ?? ''
        }]
    })
}