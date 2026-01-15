import type { Router } from "vue-router";
import type { Ref } from "vue";

import { API_ROUTE } from "../api";

export const handleLogin = async (
    username: string,
    password: string,
    router: Router,
    errorText: Ref<string, string>
) => {
    fetch(`${API_ROUTE}/user/login/`, {
        method: "POST",
        body: JSON.stringify({
            username: username,
            password: password
        }),
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include"
    })
    .then(async (res) => {
        if (res.status == 200) {
            const data = await res.json();
            localStorage.setItem("jwt", data["token"]);
            router.push("/feed");
            return;
        }

        const errMessage = (await res.json())["message"];
        errorText.value = errMessage;
    })
    .catch((err) => {
        console.error(err);
    });
};