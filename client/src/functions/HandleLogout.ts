import type { Router } from 'vue-router';
import axios from 'axios';

export const HandleLogout = (
    router: Router,
    turnOffHeader: () => void
) => {
    axios.post('user/logout/')
    .then(() => {
        turnOffHeader();
        router.push('/join');
    });
}