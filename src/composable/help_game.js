import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
const current_layout = ref('lobby')
const is_run_game = ref(false)
const is_tutorial = ref(true)
const is_warmup = ref(false)
const game_choose = ref()
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
    Funny: {
        name: 'Funny',
        level: 4,
        atk: 6,
        currentHp: 2000,
        maxHp: 2000,
        path: '/Monster/Funny monsters',
        bg: 'bg-linear-to-br from-blue-500 to-cyan-400',
        difficulty: 'Khó'
    },
    BachTuoc: {
        name: 'Bạch tuộc cactini',
        level: 4,
        atk: 6,
        currentHp: 2000,
        maxHp: 2000,
        path: '/Monster/bachtuoc',
        bg: 'bg-linear-to-br from-green-500 to-pink-400',
        difficulty: 'Khó'
    },
    fat: {
        name: 'Chất béo khó ưa',
        level: 4,
        atk: 6,
        currentHp: 500,
        maxHp: 500,
        path: '/Monster/fat',
        bg: 'bg-linear-to-br from-green-500 to-pink-400',
        difficulty: 'Dễ'
    },
    // pochita: {
    //     name: 'Pochita',
    //     level: 4,
    //     atk: 6,
    //     currentHp: 1000,
    //     maxHp: 1000,
    //     path: '/Monster/Pochita',
    //     bg: 'bg-linear-to-br from-pink-500 to-cyan-400',
    //     difficulty: 'Trung bình'
    // },

    wolf: {
        name: 'Sói cô độc',
        level: 4,
        atk: 6,
        currentHp: 1000,
        maxHp: 1000,
        path: '/Monster/wolf',
        bg: 'bg-linear-to-br from-amber-500 to-orange-400',
        difficulty: 'Trung bình'

    },
    gost1: {
        name: 'Gost',
        level: 4,
        atk: 6,
        currentHp: 2000,
        maxHp: 2000,
        path: '/Monster/gost1',
        bg: 'bg-linear-to-br from-black to-orange-400',
        difficulty: 'Khó'

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
    const getRandomMonster = () => {
        const monsterList = Object.values(monsters.value)
        const randomIndex = Math.floor(Math.random() * monsterList.length)
        return monsterList[randomIndex]
    }
    return { get_monster, get_all_monsters, getRandomMonster }
}
export function useGameChoose() {
    const get_game_choose = () => {
        return game_choose.value
    }
    const set_game_choose = (game) => {
        game_choose.value = game
    }
    return { get_game_choose, set_game_choose }
}
const data_estimate = ref({
    good_standard: 0,
    bad_standard: 0,
    up_standard: 0,
    down_standard: 0,
    exercise_type: "",
})
export function dataOnRep() {
    const get_data_estimate = () => {
        return data_estimate
    }
    const set_data_estimate = (data) => {
        data_estimate.value.good_standard = data.good_standard
        data_estimate.value.bad_standard = data.bad_standard
        data_estimate.value.up_standard = data.up_standard
        data_estimate.value.down_standard = data.down_standard
        data_estimate.value.exercise_type = data.exercise_type
    }
    return { get_data_estimate, set_data_estimate }
}