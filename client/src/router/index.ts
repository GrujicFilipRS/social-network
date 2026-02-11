import { createRouter, createWebHistory } from 'vue-router';
import Hero from '../pages/Hero.vue';
import Join from '../pages/Join.vue';
import Feed from '../pages/Feed.vue';
import Profile from '../pages/Profile.vue';
import EditProfile from '../pages/EditProfile.vue';
import CreatePost from '../pages/CreatePost.vue';

const routes = [
    { path: '/', component: Hero },
    { path: '/join', component: Join },
    { path: '/feed', component: Feed },
    { path: '/profile', component: Profile },
    { path: '/edit_profile', component: EditProfile },
    { path: '/create_post', component: CreatePost }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
