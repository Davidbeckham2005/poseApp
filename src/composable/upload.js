// upload video 
import { open } from "@tauri-apps/plugin-dialog";
import { convertFileSrc } from "@tauri-apps/api/core";
import { ref } from 'vue'
import { useSetting } from "../store/setting.store";
import { useUser } from "../store/user.store";
import { useVideo } from "../store/video.store";
import { get_tinme_video } from "../services/app.service";
import { get_status_upload_video } from "./helpers";
import { useNavigation } from "./helpers";
import { addVideo } from "../services/app.service";


const src_video = ref()
const time_video_upload = ref()
export function useUpload() {
    const userStore = useUser()
    const settingStore = useSetting()
    const videoStore = useVideo()
    const { switch_dashbroad } = useNavigation()
    const isloading = get_status_upload_video()
    const upload = async (exercise_selected) => {
        try {
            const pathSelected = await open({
                filters: [{
                    name: "video",
                    extensions: ["mp4", "avi"]
                }]
            })

            if (pathSelected) {
                src_video.value = convertFileSrc(pathSelected)
                const encodePath = encodeURIComponent(pathSelected)
                const data = {
                    "path_video": encodePath,
                    "type": exercise_selected,
                    "isDrawing": settingStore.setting.isDrawing,
                    "isAnalyst": settingStore.setting.isAnalyst,
                    "isCheck_view": settingStore.setting.isCheck_view,
                    "Analyst_FPS": settingStore.setting.Analyst_FPS,
                    "Analyst_count": settingStore.setting.Analyst_count,
                    "Analyst_count_good": settingStore.setting.Analyst_count_good,
                    "Analyst_estimate": settingStore.setting.Analyst_estimate,
                    "Analyst_state": settingStore.setting.Analyst_state,
                    "isMake_Result": settingStore.setting.isMake_Result,
                    "weight": userStore.user.weight,
                    "height": userStore.user.height
                }
                const data_to_get_time_video = {
                    "path": encodePath
                }
                time_video_upload.value = await get_tinme_video(data_to_get_time_video)
                isloading.value = true
                const res = await addVideo(data)
                while (true) {
                    await videoStore.fetchVideo()
                    if (videoStore.get_video(res.output_path)) break
                    await new Promise(r => setTimeout(r, 500))
                }
                switch_dashbroad(res.output_path)
            }
        }
        catch (error) {
            console.log(error)
        } finally {
            isloading.value = false
        }
    }
    return { upload, src_video, time_video_upload }

}