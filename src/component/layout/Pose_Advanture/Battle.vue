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

                <!-- MONSTER SIDE - LEFT -->
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

                <!-- CAMERA & EXERCISE - MIDDLE/RIGHT -->
                <div
                    class="col-span-6 bg-black rounded-3xl border-3 border-emerald-500/50 overflow-hidden flex flex-col">
                    <CaneraView :exercise_type="current_exercise_type?.id" :currentHp="monster.currentHp"
                        @result="result_handle" @finish="finish_handle" @is_analyst_active="handle_is_analyst_active">
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
            <ExerciseSelector @send_current_exercise="handle_current_exercise_type" :start_analyst="is_start">
            </ExerciseSelector>
        </div>
        <!-- VICTORY/DEFEAT MODAL -->
        <div v-if="is_finish" class="fixed inset-0 flex items-center justify-center bg-black/90 backdrop-blur-md z-50">
            <div class="w-130 rounded-3xl bg-linear-to-b from-gray-800 to-black text-white shadow-2xl p-10 border-3 animate-in fade-in"
                :class="win ? 'border-green-500' : 'border-red-500'">

                <!-- TITLE -->
                <div class="text-center mb-8">
                    <div class="text-7xl mb-4">{{ win ? '🏆' : '💔' }}</div>
                    <h1 class="text-5xl font-black tracking-wider" :class="win ? 'text-green-400' : 'text-red-400'">
                        {{ win ? "VICTORY!" : "DEFEAT!" }}
                    </h1>
                    <p class="text-gray-400 mt-3 text-lg">
                        {{ win ? 'You defeated the monster!' : 'The monster defeated you!' }}
                    </p>
                </div>

                <!-- WORKOUT STATS -->
                <div class="space-y-3 mb-8 bg-gray-900/80 rounded-2xl p-6">
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <!-- Total Reps -->
                        <div
                            class="bg-linear-to-br from-yellow-500/20 to-yellow-600/10 rounded-lg p-4 border-2 border-yellow-500/50">
                            <p class="text-xs text-yellow-300 font-bold">TOTAL REPS</p>
                            <p class="text-3xl font-black text-yellow-400">{{ old_total }}</p>
                        </div>
                        <!-- Perfect Form Reps -->
                        <div
                            class="bg-linear-to-br from-green-500/20 to-green-600/10 rounded-lg p-4 border-2 border-green-500/50">
                            <p class="text-xs text-green-300 font-bold">PERFECT FORM</p>
                            <p class="text-3xl font-black text-green-400">{{ old_good }}</p>
                        </div>
                    </div>

                    <div
                        class="flex justify-between items-center bg-gray-800 rounded-lg px-4 py-3 border-l-4 border-purple-500">
                        <span class="text-lg font-semibold text-gray-300">Damage Dealt</span>
                        <span class="text-2xl font-black text-purple-400">{{ (monster.maxHp - monster.currentHp) || 0
                            }}</span>
                    </div>

                    <div
                        class="flex justify-between items-center bg-gray-800 rounded-lg px-4 py-3 border-l-4 border-orange-500">
                        <span class="text-lg font-semibold text-gray-300">Form Accuracy</span>
                        <span class="text-2xl font-black text-orange-400">{{ old_total > 0 ? Math.floor((old_good /
                            old_total) * 100) : 0 }}%</span>
                    </div>
                </div>

                <!-- ACTION BUTTONS -->
                <div class="flex gap-4">
                    <button @click="handle_menu"
                        class="flex-1 px-6 py-4 bg-linear-to-r from-gray-600 to-gray-700 hover:from-gray-500 hover:to-gray-600 rounded-xl text-white font-bold text-lg transition-all hover:scale-105 active:scale-95 shadow-lg">
                        ← Back to Menu
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
// import
import CaneraView from './CameraView.vue'
import ExerciseSelector from './ExerciseSelector.vue'
import menu_btn from '../../bases/menu_btn.vue'
import NavBar from './NavBar.vue'
import Warmup from './Warmup.vue';
import Trainer from '../Trainer/Trainer.vue';
import { ref, computed, shallowRef } from 'vue';
import { calculating } from '../../../composable/helpers';
import { Use_is_warmup } from '../../../composable/help_game';
import { useMonster } from '../../../composable/help_game';
import { useRouter } from 'vue-router';
const { get_state_warmup } = Use_is_warmup()
const router = useRouter()
const win = ref(true)
const is_finish = ref(false)
const finish_handle = () => {
    is_finish.value = true
}
const { get_monster } = useMonster()
const { persen } = calculating()
const is_start = ref(false)
const result_on_rep = ref(null)


// State của Quái vật
const old_total = ref(0)
const old_good = ref(0)
const user_state = ref('')
const required_state = ref('')
// hiển thị damage khi đánh trúng
const result_handle = (e) => {
    origin.value = e.origin
    // console.log(origin.value)
    // console.log('result:', e)
    result_on_rep.value = e
    // Update user current state
    user_state.value = e.state || ''
    // Set required state as opposite of current user state
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
const current_exercise_tutorial = ref()
const current_exercise_type = ref()
const handle_current_exercise_type = (attact, tutorial) => {
    current_exercise_type.value = attact
    current_exercise_tutorial.value = tutorial
    console.log(current_exercise_tutorial.value)
}

const monster = computed(() => get_monster())

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
};


// nút trở lại menu
const handle_menu = () => {
    router.push({ name: 'menu' })
}
// 3/23/2026 thiết kế progress origin cho từng bài tập
const origin = shallowRef(null)
const up_standard = ref(140)
const bad_standard = ref(32)
const good_standard = ref(90)
const down_standard = ref(130)
const badWidth = computed(() => (bad_standard.value / 200) * 100);
const goodWidth = computed(() => (good_standard.value / 200) * 100);
const dowwWidth = computed(() => (down_standard.value / 200) * 100)
const progress = computed(() => {
    let p = (origin.value) / 200
    return Math.max(0, Math.min(1, p))
})
const percent = (val) => {
    return (val / 200) * 100
}
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
