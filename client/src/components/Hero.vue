<script lang='ts' setup>

    import { useRouter } from 'vue-router';

    const router = useRouter();

    function goToJoin() {
        router.push('/join');
    }

</script>

<template>
    <div class='hero'>
        <div class='lside-hero'>
            <h1>SOCIAL</h1>
            <p>
                Explore new experiences<br />
                Form new connections<br />
                Share your story
            </p>

            <button class='primary-btn' @click='goToJoin'>JOIN NOW</button>
        </div>

        <div class='rside-hero'>
            <img class='image-1' src='/hero-1.jpg' alt='' />
            <img class='image-2' src='/hero-2.jpg' alt='' />
        </div>
    </div>
</template>

<style>

@import url('./Hero.css');

</style>