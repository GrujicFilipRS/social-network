import type { Router } from 'vue-router';
import type { Ref } from 'vue';
import { eventBus } from '../events';
import axios from 'axios';
import type { UserGetData } from '../interfaces/UserGetData';

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
        const data = res.data as UserGetData;
        
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