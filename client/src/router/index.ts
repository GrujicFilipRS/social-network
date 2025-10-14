import { createRouter, createWebHistory } from 'vue-router';
import Hero from '../pages/Hero.vue';
import Join from '../pages/Join.vue';
import Feed from '../pages/Feed.vue';

// import { verifyUser } from '../api';

const routes = [
    { path: '/', component: Hero },

    { path: '/join', component: Join },

    {
        path: '/feed',
        component: Feed,
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// router.beforeEach(async (to, from, next) => {
//     if (to.meta.requiresAuth) {
//         const userId = await verifyUser();
//         if (userId === -1) return next('/');
//     }
//     next();
// })

export default router;
