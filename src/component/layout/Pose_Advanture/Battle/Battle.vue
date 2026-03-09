<template>
    <div class="min-h-screen bg-slate-900 text-white pt-3">
        <div class="bg-gray-700/50 max-w-6xl m-auto rounded-2xl p-6 mb-6 border border-gray-800 grid grid-cols-4">
            <menu_btn class="text-white"></menu_btn>
            <!-- <div class="flex-1 px-4">
                <div class="flex justify-between text-xs font-bold mb-2">
                    <span>❤️ HP</span>
                    <span>{{ stats.hp }}/{{ stats.maxHp }}</span>
                </div>
                <div class="w-full h-3 bg-gray-800 rounded-full overflow-hidden">
                    <div class="h-full bg-pink-600 rounded-full" :style="{ width: '94%' }"></div>
                </div>
            </div> -->
            <button class="btn btn-accent" @click="handleHit"></button>
        </div>

        <!-- <div class="flex-1 px-4 border-r border-gray-700">
            <div class="flex justify-between text-xs font-bold mb-2">
                <span>⚡ Stamina</span>
                <span>{{ stats.stamina }}/{{ stats.maxStamina }}</span>
            </div>
            <div class="w-full h-3 bg-gray-800 rounded-full overflow-hidden">
                <div class="h-full bg-orange-500 rounded-full" :style="{ width: '100%' }"></div>
            </div>
        </div> -->

        <!-- <div class="flex px-8 space-x-12">
            <div class="text-center">
                <p class="text-gray-500 text-[10px] uppercase font-bold">🔥 Combo</p>
                <p class="text-2xl font-black text-gray-300">{{ stats.combo }}x</p>
            </div>
            <div class="text-center">
                <p class="text-gray-500 text-[10px] uppercase font-bold">✨ Modifier</p>
                <p class="text-sm text-gray-500 italic mt-1 font-medium">No modifier</p>
            </div>
        </div> -->


        <div class="max-w-6xl m-auto grid grid-cols-12 mb-4 gap-4">
            <div class="col-span-5 rounded-3xl border relative border-red-800  flex flex-col overflow-hidden p-5">
                <!-- <div class="p-6 text-center">
                    <h2 class="text-2xl font-bold tracking-tight">{{ monster.name }}</h2>
                    <p class="text-gray-500 text-sm font-medium">Level {{ monster.level }} · ATK {{ monster.atk }}
                    </p>
                </div> -->

                <div class="rounded-3xl" :class="{
                    'bg-green-500/30': hpPercentage >= 75,
                    'bg-orange-400/30': hpPercentage < 75 && hpPercentage >= 25,
                    'bg-red-600/70 animate-pulse': hpPercentage <= 25 && hpPercentage > 0,
                    'animate-shake border-red-500/70 border-2': show_damage,
                    'animate-death': monster.currentHp == 0
                }">
                    <div class="w-[70%] max-w-6xl m-auto">
                        <div class="flex justify-between items-end">
                            <span class="text-sm font-bold text-red-500">LV. {{ monster.level }}</span>
                            <h2 class="text-xl font-black tracking-tighter">{{ monster.name }}</h2>
                            <span class="text-sm text-gray-400">HP {{ monster.currentHp }}/{{ monster.maxHp
                                }}</span>
                        </div>

                        <div class="max-w-3xl w-full h-6 bg-gray-700 rounded-full border-2 border-gray-600 p-0.5">
                            <div class="h-full bg-gradient-to-r from-orange-500 to-red-600 rounded-full"
                                :style="{ width: (monster.currentHp / monster.maxHp * 100) + '%' }"></div>
                        </div>
                    </div>
                    <Trainer>
                    </Trainer>
                    <div v-if="show_damage"
                        class="absolute inset-0 flex items-center justify-center mt-10 pointer-events-none">
                        <span
                            class="text-4xl font-medium text-white animate-bounce drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)]">
                            -{{ finnal_damage }}
                        </span>
                    </div>
                </div>
            </div>
            <div
                class="col-span-7 bg-[#0a0a0a] rounded-3xl flex flex-col px-10 justify-center relative border border-white/20">
                <Live @result="result_handle" :exercise_type="current_exercise_type?.id"
                    @is_analyst="handle_send_analyst">
                </Live>
                <!-- <div class="text-center max-w-sm">
                <div class="mb-4 flex justify-center">
                    <div class="w-16 h-16 rounded-full border-4 border-red-500 flex items-center justify-center">
                        <span class="text-red-500 text-3xl font-bold">✕</span>
                    </div>
                </div>
                <h3 class="text-xl font-bold mb-2">Camera Access Denied</h3>
                <p class="text-gray-500 text-sm mb-8 leading-relaxed">
                    Camera access denied. Using simulated pose detection instead.
                </p>

                <div class="bg-[#1a1a1a] p-6 rounded-2xl text-left border border-gray-800 mb-8">
                    <p class="text-xs text-gray-400 font-bold uppercase mb-3">To enable camera:</p>
                    <ul class="text-xs text-gray-400 space-y-2 list-decimal list-inside">
                        <li>Click the camera icon in your browser bar</li>
                        <li>Select "Allow" or "Always allow"</li>
                        <li>Reload and restart battle</li>
                    </ul>
                </div>

                <p class="text-cyan-400 text-xs font-medium mb-6 flex items-center justify-center">
                    <span class="mr-2">✨</span> Game continues with simulated detection!
                </p>

                <button
                    class="bg-[#00b4d8] hover:bg-[#0096b4] text-black font-bold py-3 px-10 rounded-xl transition-all active:scale-95">
                    Try Again
                </button>
            </div> -->
            </div>
        </div>
        <ExerciseSelector @send_current_exercise="handle_current_exercise_type" :start_analyst="is_start">
        </ExerciseSelector>
    </div>



</template>
<script setup>
import ExerciseSelector from './ExerciseSelector.vue';
import Live from '../../Live/Live.vue';
import menu_btn from '../../../bases/menu_btn.vue';
import Trainer from '../../Trainer/Trainer.vue';
import { ref, computed, watch } from 'vue';
import { calculating, get_translate } from '../../../../composable/helpers';
const { persen } = calculating()
const is_start = ref(false)
// State của Quái vật
const old_total = ref(0)
const old_good = ref(0)
const result_handle = (e) => {
    if (e.total != old_total.value) {
        if (e.good != old_good.value) {
            old_good.value = e.good
            finnal_damage.value = normal_damage.value * 1.2
        }
        handleHit()
    }
    old_total.value = e.total
}
const handle_send_analyst = (e) => {
    console.log("in battle", e)
    is_start.value = e
}
const current_exercise_type = ref()
const handle_current_exercise_type = (attact) => {
    current_exercise_type.value = attact
}
const monster = ref({
    name: 'Rock Golem',
    level: 4,
    atk: 6,
    currentHp: 200,
    maxHp: 200
});

const stats = ref({
    hp: 94,
    maxHp: 100,
    stamina: 100,
    maxStamina: 100,
    combo: 0
});
// State của bài tập
// const exercise = ref({
//     name: 'Squats',
//     target: 20,
//     completed: 12
// });

// const damageHistory = ref([]);

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
</script>

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
