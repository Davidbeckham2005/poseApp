import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
const current_layout = ref('lobby')
const is_run_game = ref(false)
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

