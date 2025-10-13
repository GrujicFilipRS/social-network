<script setup lang='ts'>

import { ref, reactive } from 'vue';

const signupMode = ref(true);

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
    console.log(formData);
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

            <p>Your name</p>
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

            <p><b>Confirm password</b></p>
            <input
                v-show='signupMode'
                type='password'
                v-model='formData.confirmPassword'
                placeholder='Confirm your password'
            />
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