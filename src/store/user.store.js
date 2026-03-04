import { defineStore } from "pinia";
import { get_user, update_user } from "../services/app.service";
import { ref, computed } from "vue";

export const useUser = defineStore('user', () => {
    const user = ref()

    const fetchUser = async () => {
        try {
            const res = await get_user()
            user.value = res.user
            // console.log(user.value)
        } catch (error) {
            console.log(error)
        }
    }
    return {
        fetchUser, user
    }
})