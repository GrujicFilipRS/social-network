import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const Follow = async (
    userId: string,
    setFollowed: (val: boolean) => void,
    errorToast?: (message: string) => void
) => {
    // Optimistic
    setFollowed(true);

    axios.post(`follow/follow_user/${userId}`)
    .then(async res => {
        const data = res.data as DTO;

        if (data.success) return;

        setFollowed(false);
        if (errorToast) errorToast(data.message ?? 'Error while following user');
    })
    .catch(() => {
        setFollowed(false);
        if (errorToast) errorToast('Error while following user');
    });
}

export const Unfollow = async (
    userId: string,
    setFollowed: (val: boolean) => void,
    errorToast?: (message: string) => void
) => {
    // Optimistic
    setFollowed(false);

    axios.delete(`follow/unfollow_user/${userId}`)
    .then(async res => {
        const data = res.data as DTO;

        if (data.success) return;

        setFollowed(true);
        if (errorToast) errorToast(data.message ?? 'Error while unfollowing user');
    })
    .catch(() => {
        setFollowed(true);
        if (errorToast) errorToast('Error while following user');
    });
}