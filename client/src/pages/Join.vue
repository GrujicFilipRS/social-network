<script setup lang='ts'>

import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { API_ROUTE } from '../api';

const router = useRouter();

const signupMode = ref(true);
const errorText = ref('');

interface SignupData {
    username: string;
    name: string;
    password: string;
    confirmPassword: string;
};

const formData = reactive<SignupData>({
    username: '',
    name: '',
    password: '',
    confirmPassword: ''
});

const submitSignup = () => {
    if (signupMode) {
        if (formData.password == formData.confirmPassword)
            handleSignup(formData.username.toLowerCase(), formData.password);
    }
    else {
        handleLogin();
    }
}

const handleSignup = (username: string, password: string) => {
    fetch(`${API_ROUTE}/user/register/`, {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            password: password
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(async (res) => {
        if (res.status == 201) {
            const data = await res.json();
            localStorage.setItem('jwt', data['token']);
            router.push('/feed');
            return;
        }
    
        const errMessage = (await res.json())['message'];
        errorText.value = errMessage;
    }).catch((err) => {

    })
}

const handleLogin = () => {

}

</script>

<template>

<div class='join'>
    <img src='/signup-image.jpg' />
    <div class='form'>
        <div class='inputs'>
            <p><b>Username</b></p>
            <input
                type='text'
                v-model='formData.username'
                placeholder='Enter your username'
            />

            <p v-show='signupMode'>Your name</p>
            <input
                v-show='signupMode'
                type='text'
                v-model='formData.name'
                placeholder='Enter your name (not required)'
            />
            
            <p><b>Your password</b></p>
            <input
                type='password'
                v-model='formData.password'
                placeholder='Enter your password'
                
            />

            <p v-show='signupMode'><b>Confirm password</b></p>
            <input
                v-show='signupMode'
                type='password'
                v-model='formData.confirmPassword'
                placeholder='Confirm your password'
            />

            <p class='red-color error-text'>{{errorText}}</p>
        </div>
        
        <div class='buttons'>
            <button
                class='primary-btn'
                @click='submitSignup'
            >
                {{ signupMode ? 'Sign up' : 'Log in' }}
            </button>

            <p>OR</p>

            <button
                class='secondary-btn'
                @click='signupMode=!signupMode'
            >
                {{ signupMode ? 'Log in' : 'Sign up' }}
            </button>   
        </div>
    </div>
</div>

</template>

<style>

@import url('./Join.css');

</style>