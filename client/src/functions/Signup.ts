import type { Router } from 'vue-router';
import type { Ref } from 'vue';
import { eventBus } from '../events';
import type { DTO } from '../interfaces/DTO';
import axios from 'axios';

export const handleSignup = async (
    username: string,
    password: string,
    name: string | null,
    router: Router,
    errorText: Ref<string, string>
) => {
    if (name === '') name = null;

    const registrationData = {
        username: username,
        password: password,
        name: name
    }

    axios.post('user/register/', registrationData)
    .then(async (res) => {
        const data = res.data as DTO;
        
        if (data.success) {
            router.push('/feed');
            eventBus.emit('header-update');
            return;
        }

        const errMessage = data.message;
        errorText.value = errMessage ?? 'An error occurred during registration.';
    }).catch((_) => {
        errorText.value = 'An error occurred during registration.';
    });
}