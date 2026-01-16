<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { verifyUser } from "../api";

import { handleSignup } from "../functions/Signup";
import { handleLogin } from "../functions/Login";

const router = useRouter();

const verificationData = await verifyUser();
if (verificationData.statusCode !== 200) {
    router.push('/join');
}

const signupMode = ref(true);
const errorText = ref("");

interface SignupData {
    username: string;
    name: string;
    password: string;
    confirmPassword: string;
}

const formData = reactive<SignupData>({
    username: "",
    name: "",
    password: "",
    confirmPassword: "",
});

async function submitSignup() {
    if (signupMode.value) {
        if (formData.password != formData.confirmPassword) {
            errorText.value = "The confirmation must match the password"
            return;
        }

        await handleSignup(
            formData.username.toLowerCase(),
            formData.password,
            formData.name,
            router,
            errorText
        );
    } else {
        await handleLogin(
            formData.username.toLowerCase(),
            formData.password,
            router,
            errorText
        );
    }
};

</script>

<template>
    <div class="join">
        <img src="/signup-image.jpg" />
        <div class="form">
            <div class="inputs">
                <p><b>Username</b></p>
                <input
                    type="text"
                    v-model="formData.username"
                    placeholder="Enter your username"
                />

                <p v-show="signupMode">Your name</p>
                <input
                    v-show="signupMode"
                    type="text"
                    v-model="formData.name"
                    placeholder="Enter your name (not required)"
                />

                <p><b>Your password</b></p>
                <input
                    type="password"
                    v-model="formData.password"
                    placeholder="Enter your password"
                />

                <p v-show="signupMode"><b>Confirm password</b></p>
                <input
                    v-show="signupMode"
                    type="password"
                    v-model="formData.confirmPassword"
                    placeholder="Confirm your password"
                />

                <p class="red-color error-text">{{ errorText }}</p>
            </div>

            <div class="buttons">
                <button class="primary-btn" @click="submitSignup">
                    {{ signupMode ? "Sign up" : "Log in" }}
                </button>

                <p>OR</p>

                <button class="secondary-btn" @click="signupMode = !signupMode">
                    {{ signupMode ? "Log in" : "Sign up" }}
                </button>
            </div>
        </div>
    </div>
</template>

<style>
@import url("./Join.css");
</style>
