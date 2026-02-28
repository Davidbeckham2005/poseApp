import { api } from "../api";
// const ws = new WebSocket("ws://localhost:8000/ws")
// ws.onopen = () => {
//     console.log("connected")
// }
// ws.onmessage = (e) => {
//     const data = JSON.parse(e.data)
//     console.log(data)
// }

export async function getHello() {
    return await api.get("/hello").data
}
// export async function getResult() {
//     return (await api.get("/result")).data
// }
export async function getId(id) {
    return (await api.get(`/video/get/${id}`)).data
}
// export async function readFile(path) {
//     const encodePath = encodeURIComponent(path)
//     return (await api.get(`/file/${encodePath}`)).data
// }
export async function addVideo(data) {
    return (await api.post("/video/add", data)).data
}

export async function get_video(filename) {
    return (await api.get(`/video/get/${filename}`)).data

}
export async function get_all_video() {
    return (await api.get('/video/get_all')).data
}
export async function get_setting() {
    return (await api.get('/setting/get')).data
}
export async function delete_video(data_video) {
    return (await api.delete("/video/delete", { data: data_video })).data
}
export async function delete_videos(data_video) {
    return (await api.delete("/video/delete_select", { data: data_video })).data
}
export async function show_camera(data_video) {
    return (await api.post("/service/show_camera", data_video)).data
}