<template>
    <div class="min-h-screen overflow-scroll bg-linear-to-b from-gray-900 to-black text-white pt-10">
        <menu_btn class="text-white absolute top-3 left-3 z-50"></menu_btn>
        <NavBar></NavBar>
        <Warmup v-if="get_state_warmup()"></Warmup>
        <div v-else class="relative w-full h-screen flex flex-col">
            <div class="p-10 bg-slate-900 flex flex-col items-center">
                <div class="relative w-full max-w-xl h-6 bg-slate-700 rounded- border border-slate-600 overflow-hidden">
                    <div class="absolute left-0 h-full bg-red-600/30 border-x border-red-500/50" :style="{
                        width: badWidth + '%',
                    }">
                    </div>
                    <div class="absolute  h-full bg-green-600/30 border-x border-red-500/50" :style="{
                        width: goodWidth + '%', left: badWidth + '%'
                    }">
                    </div>
                    <div class="absolute  h-full bg-orange-600/30 border-x border-red-500/50" :style="{
                        width: dowwWidth + '%', left: goodWidth + '%'
                    }">
                    </div>

                    <div class="absolute top-0 h-full bg-blue-400 w-1 z-10" :style="{
                        left: progress * 100 + '%',

                    }">
                    </div>
                </div>
                <p class="mt-4 text-slate-500 font-mono text-xs uppercase tracking-widest">
                    Power: {{ (progress * 100).toFixed(0) }}%
                </p>
            </div>
            <div class="flex-1 grid grid-cols-12 gap-4 p-4">
                <div class="col-span-3 flex flex-col justify-center">
                    <div class="rounded-3xl border-3 border-red-600 relative overflow-hidden p-4 bg-linear-to-b from-red-900/20 to-black"
                        :class="[
                            hpPercentage >= 75 ? monster.bg : '',
                            hpPercentage < 75 && hpPercentage >= 25 ? 'dark:bg-orange-400/20' : '',
                            hpPercentage <= 25 && hpPercentage > 0 ? 'bg-red-600/40 animate-pulse' : '',
                            show_damage ? 'animate-shake border-red-500 border-4' : '',
                            monster.currentHp == 0 ? 'animate-death' : ''
                        ]">

                        <!-- MONSTER NAME & HP -->
                        <div class="mb-4">
                            <div class="flex justify-between items-center mb-2">
                                <h2 class="text-3xl font-black tracking-tighter text-red-400">{{ monster.name }}</h2>
                                <span class="px-4 py-2 rounded-full text-sm font-black bg-red-500/80 text-white">
                                    ❤️ {{ monster.currentHp }}/{{ monster.maxHp }}
                                </span>
                            </div>
                            <!-- HP BAR -->
                            <div
                                class="w-full h-8 bg-gray-700 rounded-full border-2 border-gray-600 p-1 overflow-hidden">
                                <div class="h-full bg-liear-to-r from-orange-500 to-red-600 rounded-full transition-all duration-300"
                                    :style="{ width: (monster.currentHp / monster.maxHp * 100) + '%' }"></div>
                            </div>
                        </div>
                        <Trainer :path_json="monster.path">
                        </Trainer>
                        <div v-if="show_damage"
                            class="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <span
                                class="text-6xl font-black text-red-400 animate-bounce drop-shadow-[0_4px_12px_rgba(255,0,0,0.8)]">
                                -{{ finnal_damage }}
                            </span>
                        </div>
                    </div>
                </div>
                <!-- MONSTER SIDE - LEFT -->
                <!-- CAMERA & EXERCISE - MIDDLE/RIGHT -->
                <div
                    class="col-span-6 bg-black rounded-3xl border-3 border-emerald-500/50 overflow-hidden flex flex-col">
                    <CaneraView :exercise_type="current_exercise_type?.id" @result="result_handle"
                        @finish="finish_handle" @is_analyst_active="handle_is_analyst_active">
                    </CaneraView>
                </div>

                <div class="col-span-3 flex flex-col justify-center gap-4">
                    <div class="bg-linear-to-b from-blue-900/40 to-black rounded-3xl border-3 p-6 flex flex-col items-center justify-center min-h-75"
                        :class="required_state === 'up' ? 'border-green-400' : 'border-orange-400'">
                        <!-- Required State -->
                        <div v-if="required_state" class="text-center">
                            <p class="text-sm text-yellow-300 font-bold mb-6">NEXT ACTION</p>
                            <div class="flex items-center justify-center h-32 w-32 rounded-full border-4  bg-yellow-900/30"
                                :class="required_state === 'up' ? 'border-green-400' : 'border-orange-400'">
                                <div class="text-7xl font-black"
                                    :class="required_state === 'up' ? 'text-green-400' : 'text-orange-400'">
                                    {{ required_state === 'up' ? '↑' : '↓' }}
                                </div>
                            </div>
                        </div>
                        <div v-else class="text-center">
                            <p class="text-sm text-gray-400 font-bold">Bắt đầu phân tích để xem hướng dẫn
                                <span>{{ normal_damage }}</span>
                            </p>
                        </div>

                    </div>

                </div>
            </div>

            <!-- EXERCISE SELECTOR - BOTTOM OVERLAY -->
            <div v-if="is_start && !is_finish && currentExercise" class="fixed top-20 right-6 w-48 bg-gray-900/90 backdrop-blur-md rounded-2xl border-2 border-blue-500/50 p-2
            shadow-2xl animate-in slide-in-from-right duration-500 z-40">

                <div
                    class="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1 px-1 flex justify-between">
                    <span>Current Form</span>
                    <span class="animate-pulse">● LIVE</span>
                </div>

                <div class="relative w-full aspect-square bg-black rounded-xl overflow-hidden border border-gray-800">
                    <img :src="currentExercise.gif" class="w-full h-full object-cover opacity-90" />

                    <div class="absolute bottom-0 inset-x-0 bg-linear-to-t from-black via-black/70 to-transparent p-2">
                        <p class="text-[10px] text-blue-200 font-bold leading-tight mb-1">
                            {{ currentExercise.title }}
                        </p>
                        <p class="text-[9px] text-gray-300 leading-tight italic">
                            "{{ currentExercise.proTip }}"
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <Summary v-if="is_finish" :summary="summary" :win="win"></Summary>
    </div>
</template>
<script setup>
// import
import CaneraView from './CameraView.vue'
import menu_btn from '../../bases/menu_btn.vue'
import NavBar from './NavBar.vue'
import Warmup from './Warmup.vue';
import Trainer from '../Trainer/Trainer.vue';
import { ref, computed, shallowRef, watch } from 'vue';
import { calculating } from '../../../composable/helpers';
import { Use_is_warmup } from '../../../composable/help_game';
import { useMonster } from '../../../composable/help_game';
import { useRouter } from 'vue-router';
import Summary from './Summary.vue';
import { useExercise } from '../../../constants/exercise'
import { useAudio } from '../../../composable/audio'
const { get_exercise } = useExercise()
const { stopSpeak } = useAudio()
const { get_state_warmup } = Use_is_warmup()
const router = useRouter()
const currentExercise = computed(() => get_exercise(current_exercise_type.value))
const current_exercise_type = ref(null)
const is_finish = ref(false)
const summary = ref(null)
const finish_handle = (data) => {
    stopSpeak()
    is_finish.value = true
    summary.value = data
    console.log('workout summary:', summary.value)
}
const { get_monster, get_all_monsters } = useMonster()
const { persen } = calculating()
const is_start = ref(false)
const result_on_rep = ref(null)


const old_total = ref(0)
const old_good = ref(0)
const user_state = ref('')
const required_state = ref('')
const result_handle = (e) => {
    current_exercise_type.value = e.exercise_type
    origin.value = e.origin
    result_on_rep.value = e
    user_state.value = e.state || ''
    required_state.value = e.state === 'up' ? 'down' : (e.state === 'down' ? 'up' : '')

    if (e.total != old_total.value) {
        if (e.good != old_good.value) {
            old_good.value = e.good
            finnal_damage.value = normal_damage.value * 2
        }
        handleHit()
    }
    old_total.value = e.total
}
const handle_is_analyst_active = (e) => {
    is_start.value = e
    console.log('is_start:', is_start.value)
}
// xử lý chọn bài tập
// const current_exercise_type = ref()


const monster = computed(() => get_all_monsters().dragon)

// Tính toán phần trăm máu
const hpPercentage = computed(() => (persen(monster.value.currentHp, monster.value.maxHp)));
const normal_damage = computed(() => (current_exercise_type.value?.damage || 0))
const finnal_damage = ref(normal_damage.value)
const show_damage = ref(false)
const handleHit = async () => {
    if (monster.value.currentHp > 0) {
        monster.value.currentHp -= finnal_damage.value;
        show_damage.value = true
        await new Promise(r => setTimeout(r, 500))
        show_damage.value = false

        if (monster.value.currentHp < 0) {
            monster.value.currentHp = 0
        }
    }
    finnal_damage.value = normal_damage.value
}
import { dataOnRep } from '../../../composable/help_game'
const { set_data_on_rep, get_data_estimate } = dataOnRep()
const data_estimate = get_data_estimate()

// 3/23/2026 thiết kế progress origin cho từng bài tập
const origin = shallowRef(0)
const badWidth = computed(() => ((data_estimate.value?.bad_standard || 0) / 200) * 100);
const goodWidth = computed(() => ((data_estimate.value?.good_standard || 0) / 200) * 100);
const dowwWidth = computed(() => ((data_estimate.value?.down_standard || 0) / 200) * 100);
console.log('badWidth:', badWidth.value, 'goodWidth:', goodWidth.value, 'dowwWidth:', dowwWidth.value)
const progress = computed(() => {
    let p = (origin.value) / 200
    return Math.max(0, Math.min(1, p))
})

</script>

<!-- css không liên quan -->
<style scoped>
@keyframes shake-left {
    0% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-10px);
    }

    50% {
        transform: translateX(10px);
    }

    75% {
        transform: translateX(-5px);
    }

    100% {
        transform: translateX(0);
    }
}

.animate-shake {
    animation: shake-left 0.3s ease-in-out;
}

@keyframes death-fall {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }

    25% {
        transform: translateY(-10px) rotate(-5deg);
    }

    100% {
        transform: translateY(100px) rotate(20deg);
        opacity: 0;
    }
}

.animate-death {
    animation: death-fall 0.8s forwards ease-in;
}
</style>
