
import { ref } from 'vue'
const is_show_skeleton = ref(true)
export function useSkeleton() {
    const get_skeleton = () => { return is_show_skeleton.value }
    const set_skeleton = () => { is_show_skeleton.value = !is_show_skeleton.value }
    return { get_skeleton, set_skeleton }
}
const is_show_analyst = ref(true)
export function use_analyst() {
    const get_analyst = () => { return is_show_analyst.value }
    const set_analyst = () => { is_show_analyst.value = !is_show_analyst.value }
    return { get_analyst, set_analyst }
}
const is_analysting = ref(false)
export function use_analysting() {
    const get_analysting = () => { return is_analysting.value }
    const set_analysting = (value) => { is_analysting.value = value }
    return { get_analysting, set_analysting }
}