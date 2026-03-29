import { createRouter, createWebHistory } from "vue-router";
import Home from "../Home.vue";
import Menu from "../component/layout/Pose_Advanture/menu.vue"
import Battle from "../component/layout/Pose_Advanture/Battle.vue";
import game_1 from "../component/layout/Pose_Advanture/game_1.vue";
import game_2 from "../component/layout/Pose_Advanture/Battle_2.vue";
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
    },
    {
        path: "/game/game_1",
        component: game_1,
        name: 'game_1',
    },
    {
        path: "/game/game_2",
        component: game_2,
        name: 'game_2',
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})
export default router