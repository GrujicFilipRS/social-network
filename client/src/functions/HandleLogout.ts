import type { Router } from 'vue-router';
import { Fetch } from '../api';

export const HandleLogout = (
    router: Router,
    turnOffHeader: () => void
) => {
    Fetch('user/logout/', { method: 'POST' })
    .then(() => {
        turnOffHeader();
        router.push('/join');
    });
}