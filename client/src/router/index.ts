import { createRouter, createWebHistory } from 'vue-router';
import Hero from '../pages/Hero.vue';
import Join from '../pages/Join.vue';

const routes = [
    { path: '/', component: Hero },
    { path: '/join', component: Join }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
