import { createRouter, createWebHistory } from "vue-router";
import Home from "../Home.vue";
import Menu from "../component/layout/Pose_Advanture/menu.vue"
import Battle from "../component/layout/Pose_Advanture/Battle.vue";
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
    },
    {
        path: "/game/battle/:monster",
        component: Battle,
        name: 'battle'
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})
export default router