import type { Router } from "vue-router";
import { API_ROUTE } from "../api";
import type { Ref } from "vue";

export async function handleSignup (
    username: string,
    password: string,
    router: Router,
    errorText: Ref<string, string>
) {
    fetch(`${API_ROUTE}/user/register/`, {
        method: "POST",
        body: JSON.stringify({
            username: username,
            password: password,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(async (res) => {
        if (res.status == 201) {
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
}