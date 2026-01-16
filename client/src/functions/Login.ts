import type { Router } from "vue-router";
import type { Ref } from "vue";

import { Fetch } from "../api";

export const handleLogin = async (
    username: string,
    password: string,
    router: Router,
    errorText: Ref<string>
) => {
    Fetch('user/login/', {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            password: password
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
};