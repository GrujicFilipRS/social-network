import { createRouter, createWebHistory } from 'vue-router';
import Hero from '../pages/Hero.vue';
import Join from '../pages/Join.vue';
import Feed from '../pages/Feed.vue';
import Profile from '../pages/Profile.vue';

const routes = [
    { path: '/', component: Hero },
    { path: '/join', component: Join },
    { path: '/feed', component: Feed },
    { path: '/profile', component: Profile }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
