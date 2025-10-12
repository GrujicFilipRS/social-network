import { createRouter, createWebHistory } from "vue-router";
import Hero from "../components/Hero.vue";

const routes = [
    { path: "/", component: Hero }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
