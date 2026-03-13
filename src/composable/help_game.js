import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
const current_layout = ref('lobby')
const is_run_game = ref(false)
const is_tutorial = ref(true)
const is_warmup = ref(false)
export function useNavigation() {
    const get_current_layout = () => {
        return current_layout.value
    }
    const swich_current_layout = (layout) => {
        current_layout.value = layout
        console.log(current_layout.value)
    }
    return { get_current_layout, swich_current_layout }
}
export function state_game() {

    const get_state_game = computed(() => {
        return is_run_game.value
    })
    const set_state_game = (value) => {
        is_run_game.value = value
    }
    return { get_state_game, set_state_game }
}
export function Usetutorial() {
    const get_state_tutorial = () => { return is_tutorial.value }
    const set_state_tutorial = (state) => {
        is_tutorial.value = state
    }
    return { get_state_tutorial, set_state_tutorial }
}
export function Use_is_warmup() {
    const get_state_warmup = () => {
        return is_warmup.value
    }
    const set_state_warmup = (state) => {
        is_warmup.value = state
    }
    return { get_state_warmup, set_state_warmup }
}
const monsters = ref({
    dragon: {
        name: 'Dragon',
        level: 4,
        atk: 6,
        currentHp: 20000,
        maxHp: 20000,
        path: '/Monster/dragon',
        bg: 'bg-gradient-to-br from-blue-500 to-cyan-400'
    },
    dancer: {
        name: 'dancer',
        level: 4,
        atk: 6,
        currentHp: 200,
        maxHp: 200,
        path: '/Monster/dancer',
        bg: 'bg-gradient-to-br from-red-500 to-cyan-400'
    },
    CactiniSandalini: {
        name: 'Cactini Sandalini',
        level: 4,
        atk: 6,
        currentHp: 200,
        maxHp: 200,
        path: '/Monster/Monster 3',
        bg: 'bg-gradient-to-br from-green-500 to-cyan-400'

    },
    pochita: {
        name: 'Pochita',
        level: 4,
        atk: 6,
        currentHp: 200,
        maxHp: 200,
        path: '/Monster/Pochita',
        bg: 'bg-gradient-to-br from-pink-500 to-cyan-400'
    },
    // slime: {
    //     name: 'Slime',
    //     level: 4,
    //     atk: 6,
    //     currentHp: 200,
    //     maxHp: 200,
    //     path: '/Monster/slime',
    //     bg: 'bg-gradient-to-br from-red-500 to-blue-400'

    // },
    wolf: {
        name: 'Wolf',
        level: 4,
        atk: 6,
        currentHp: 200,
        maxHp: 200,
        path: '/Monster/wolf',
        bg: 'bg-gradient-to-br from-amber-500 to-orange-400'

    },
    gost1: {
        name: 'Gost',
        level: 4,
        atk: 6,
        currentHp: 200,
        maxHp: 200,
        path: '/Monster/gost1',
        bg: 'bg-gradient-to-br from-black to-orange-400'

    },
});
export function useMonster() {
    const route = useRoute()
    const get_monster = () => {
        const monster_name = computed(() => {

            return route.params.monster
        })
        console.log(monster_name.value)
        return monsters.value[monster_name.value]
    }
    const get_all_monsters = () => {
        return monsters.value
    }
    return { get_monster, get_all_monsters }
}