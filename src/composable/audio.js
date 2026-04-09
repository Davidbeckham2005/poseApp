import { ref, watch } from 'vue'

// ĐƯA BIẾN RA NGOÀI: Để tất cả component dùng chung 1 trạng thái duy nhất
const audioEnabled = ref(true)
const currentTrack = ref(null)

let audioUnlocked = false
const globalVolume = ref(1)
const sounds = {
    rep: new Audio(('/sounds/ding.mp3')),
    success: new Audio(('/sounds/success.mp3')),

}
const bg = {
    cartoon: new Audio(('/sounds/cartoon_music.mp3')),
    moti_music: new Audio(('/sounds/moti_music.mp3')),
    Mic_Drop: new Audio(('/sounds/mic_drop.mp3'))
}
const tracks = ['cartoon', 'moti_music', 'Mic_Drop']
// Theo dõi biến để hủy speech ngay lập tức khi tắt
watch(audioEnabled, (newVal) => {
    if (!newVal) {
        window.speechSynthesis.cancel()
        console.log('🔈 Audio: Toàn bộ hàng đợi đã được hủy.')
    }
})
export const playSound = (type) => {
    const sound = sounds[type]
    if (sound && audioEnabled.value) {
        Object.values(sounds).forEach(s => {
            s.pause(); s.currentTime = 0;
        })
        sound.play().catch(e => console.log("Audio play blocked", e));
    }
}
export function useAudio() {
    const unlockAudio = () => {
        if (audioUnlocked) return
        const speech = new SpeechSynthesisUtterance("")
        window.speechSynthesis.speak(speech)
        audioUnlocked = true
    }
    const speak = (text) => {
        if (!window.speechSynthesis) return
        window.speechSynthesis.cancel()
        const utter = new SpeechSynthesisUtterance(String(text))
        utter.lang = "vi-VN"
        utter.rate = 1.1 // Đọc nhanh hơn một chút để bắt kịp nhịp tập
        utter.pitch = 1
        window.speechSynthesis.speak(utter)
    }
    const stopSpeak = () => window.speechSynthesis.cancel()
    const toggleAudio = () => audioEnabled.value = !audioEnabled.value

    const playBGM = (name) => {
        if (!audioEnabled.value) return
        Object.values(bg).forEach(b => {
            b.pause(); b.currentTime = 0;
        })

        const bgm = bg[name]
        if (bgm) {
            currentTrack.value = name
            bgm.loop = true
            bgm.volume = globalVolume.value
            bgm.play().catch(e => console.log("BGM play blocked", e));
        }
    }
    const stopBGM = () => {
        Object.values(bg).forEach(b => {
            b.pause(); b.currentTime = 0;
        })
    }
    const set_background_music_volume = (val) => {
        Object.values(bg).forEach(b => {
            b.volume = val
        })
    }
    const isAudioEnabled = () => { audioEnabled.value }
    return { unlockAudio, speak, toggleAudio, isAudioEnabled, stopSpeak, playBGM, stopBGM, set_background_music_volume, currentTrack, tracks }
}