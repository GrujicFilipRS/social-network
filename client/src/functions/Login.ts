import type { Router } from 'vue-router';
import type { Ref } from 'vue';

import { eventBus } from '../events';
import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const handleLogin = async (
    username: string,
    password: string,
    router: Router,
    errorText: Ref<string>
) => {
    axios.post('user/login/', {
        username: username,
        password: password
    }).then(async (res) => {
        const data = res.data as DTO;
        
        if (data.success) {
            router.push('/feed');
            eventBus.emit('header-update');
            return;
        }

        const errMessage = data.message;
        errorText.value = errMessage ?? 'An error occurred during login.';
    }).catch((_) => {
        errorText.value = 'An error occurred during login.';
    });
};