import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
const is_upload_video = ref(false)

export function useNavigation() {
    const route = useRoute()
    const router = useRouter()

    const switch_on_sidebar = (name) => {
        router.push({
            path: "/",
            query: {
                tab: name
            }
        })
    }

    const currentTab = computed(() => {
        return route.query.tab
    })
    const currentFile = computed(() => {
        return route.query.filename
    })
    const switch_dashbroad = (path_video) => {
        router.push({
            path: "/",
            query: {
                tab: "dashboard",
                filename: path_video
            }
        })

    }
    return { switch_on_sidebar, currentTab, switch_dashbroad, currentFile }
}
export function get_translate() {
    const from_under = {
        enterActiveClass: "transition duration-1000 ease-out",
        enterFromClass: "transform translate-y-10 opacity-0",
        enterToClass: "transform translate-y-0 opacity-100",
        leaveActiveClass: "transition duration-100 ease-in",
        leaveFromClass: "transform translate-y-0 opacity-100",
        leaveToClass: "transform translate-y-10 opacity-0",
        mode: "out-in"

    }
    const from_left = {
        enterActiveClass: "transition-all duration-700 ease-out",
        enterFromClass: "-translate-x-full opacity-0",
        enterToClass: "translate-x-0 opacity-100",
        leaveActiveClass: "transition-all duration-500 ease-in",
        leaveFromClass: "translate-x-0 opacity-100",
        leaveToClass: "-translate-x-full opacity-0",
        mode: "out-in"
    }
    const only_from_left = {
        leaveActiveClass: "transition-all duration-300 ease-in",
        leaveFromClass: "translate-x-0 opacity-100",
        leaveToClass: "-translate-x-full opacity-0",
        mode: "out-in"
    }
    const from_top = {
        enterActiveClass: "transition-all duration-700 ease-out",
        enterFromClass: "-translate-y-full opacity-0",
        enterToClass: "translate-y-0 opacity-100",
        leaveActiveClass: "transition-all duration-600 ease-in-out",
        leaveFromClass: "translate-y-0 opacity-100",
        leaveToClass: "-translate-y-full opacity-0"
    }

    return {
        from_under, from_left, from_top, only_from_left
    }
}
export function get_status_upload_video() {
    return is_upload_video
}


export function calculating() {
    const persen = (value, total) => {
        return value / total * 100
    }
    return {
        persen
    }
}
