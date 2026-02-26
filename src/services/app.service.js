import { api } from "../api";

export async function getHello() {
    return await api.get("/hello").data
}
export async function getResult() {
    return (await api.get("/result")).data
}
export async function getId(id) {
    return (await api.get(`/get/${id}`)).data
}
export async function readFile(path) {
    const encodePath = encodeURIComponent(path)
    return (await api.get(`/file/${encodePath}`)).data
}
export async function addVideo(data) {
    return (await api.post("/addVideo/", data)).data
}

export async function get_video(filename) {
    return (await api.get(`/get_video/${filename}`)).data

}
export async function get_all_video() {
    return (await api.get('/get_video/')).data
}
export async function get_setting() {
    return (await api.get('/get_setting')).data
}
export async function delete_video(data_video) {
    return (await api.delete("/deleteVideo/", { data: data_video })).data
}
export async function delete_videos(data_video) {
    return (await api.delete("/deleteVideos/", { data: data_video })).data
}