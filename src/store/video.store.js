import { defineStore } from "pinia";
import { get_all_video, get_video } from "../services/app.service";
import { ref } from "vue";

export const useVideo = defineStore('video', () => {
    const videos = ref([])
    const total_video = ref(0)
    const fetchVideo = async () => {
        try {
            const res = await get_all_video()
            videos.value = res.video_items
            total_video.value = res.total
        } catch (error) {
            console.log(error)
        }
    }
    const get_video = (path) => {
        return videos.value.find(v => v.output_path === path)
    }
    return {
        fetchVideo, total_video, videos, get_video
    }
})