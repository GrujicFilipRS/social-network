import type { Router } from 'vue-router';
import { Fetch } from '../api';

export const HandleLogout = (
    router: Router,
    turnOffHeader: () => void
) => {
    Fetch('user/logout/')
    .then(() => {
        turnOffHeader();
        router.push('/join');
    });
}