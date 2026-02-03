import type { Router } from 'vue-router';
import { Fetch } from '../api';
import type { Ref } from 'vue';

export const handleSignup = async (
    username: string,
    password: string,
    name: string,
    router: Router,
    errorText: Ref<string, string>
) => {
    Fetch('user/register/', {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            password: password,
            name: name
        })
    })
    .then(async (res) => {
        if (res.status == 200) {
            router.push('/feed');
            return;
        }
        
        const errMessage = (await res.json())['message'];
        errorText.value = errMessage;
    }).catch((err) => {
        console.error(err);
    });
}