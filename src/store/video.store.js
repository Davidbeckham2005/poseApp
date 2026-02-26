import { defineStore } from "pinia";
import { get_all_video, get_video, delete_video, delete_videos } from "../services/app.service";
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
    const delete_video_store = async (data) => {
        try {
            await delete_video(data)
            videos.value = videos.value.filter(video => video.output_path !== data.output_path)

        } catch (error) {
            console.log("Loi khi xoa ", error)
        }
    }
    const delete_videos_store = async (data) => {
        try {
            await delete_videos(data)
            videos.value = videos.value.filter(video => !data.output_paths.includes(video.output_path))
        } catch (error) {
            console.log("Loi khi xoa ", error)
        }
    }

    return {
        fetchVideo, total_video, videos, get_video, delete_video_store, delete_videos_store
    }
})