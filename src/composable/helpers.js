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
    return {
        enterActiveClass: "transition duration-1000 ease-out",
        enterFromClass: "transform translate-y-10 opacity-0",
        enterToClass: "transform translate-y-0 opacity-100",
        leaveActiveClass: "transition duration-100 ease-in",
        leaveFromClass: "transform translate-y-0 opacity-100",
        leaveToClass: "transform translate-y-10 opacity-0",
        mode: "out-in"
    }
}
export function get_status_upload_video() {
    return is_upload_video
}

