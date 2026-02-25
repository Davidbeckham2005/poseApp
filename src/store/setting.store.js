import { defineStore } from "pinia";
import { ref } from "vue";
import { get_setting } from "../services/app.service";
export const useSetting = defineStore('setting', () => {
    const setting = ref({
        isCheck_view: true,
        isDrawing: true,
        isAnalyst: true,
    })
    const fetchSetting = async () => {
        try {
            const res = await get_setting()
            setting.value = res
        } catch (error) {
            console.log(error)
        }
    }
    const update_setting = (new_setting) => {
        setting.value = new_setting
    }
    return {
        fetchSetting, setting, update_setting
    }
})