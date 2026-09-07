import type { UserListResponse } from '../interfaces/UserListResponse';
import axios from 'axios';

export const GetUserFollows = async (userId: string) => {
    return axios.get(`follow/get_user_follows/${userId}`)
    .then(async (res) => {
        const data = res.data as UserListResponse;
        return data;
    });
}