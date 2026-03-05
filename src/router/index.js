import { createRouter, createWebHistory } from "vue-router";
import Home from "../Home.vue";
import Menu from "../component/layout/Pose_Advanture/menu.vue"
const routes = [
    {
        path: "/",
        name: 'home',
        component: Home
    },
    {
        path: "/game/menu",
        component: Menu,
        name: 'menu'
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})
export default router