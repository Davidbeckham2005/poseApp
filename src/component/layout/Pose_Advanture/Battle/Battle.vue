<template>
    <div class="min-h-screen bg-slate-900 text-white pt-3">
        <div class="bg-[#1a1a1a] max-w-6xl m-auto rounded-2xl p-6 mb-6 border border-gray-800 grid grid-cols-4">
            <menu_btn class="text-white"></menu_btn>
            <div class="flex-1 px-4">
                <div class="flex justify-between text-xs font-bold mb-2">
                    <span>❤️ HP</span>
                    <span>{{ stats.hp }}/{{ stats.maxHp }}</span>
                </div>
                <div class="w-full h-3 bg-gray-800 rounded-full overflow-hidden">
                    <div class="h-full bg-pink-600 rounded-full" :style="{ width: '94%' }"></div>
                </div>
            </div>
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


        <div class="max-w-6xl m-auto grid grid-cols-12 gap-6 ">

            <div class="col-span-5 rounded-3xl border relative border-gray-800 flex flex-col overflow-hidden" :class="{
                'bg-green-500/30': hpPercentage >= 75,
                'bg-orange-400/30': hpPercentage < 75 && hpPercentage >= 25,
                'bg-red-600/70 animate-pulse': hpPercentage <= 25 && hpPercentage > 0,
                'animate-shake': show_damage,
                'animate-death': monster.currentHp == 0

            }">

                <div class="p-6 text-center">
                    <h2 class="text-2xl font-bold tracking-tight">{{ monster.name }}</h2>
                    <p class="text-gray-500 text-sm font-medium">Level {{ monster.level }} · ATK {{ monster.atk }}
                    </p>
                </div>
                <Trainer>
                </Trainer>
                <div v-if="show_damage"
                    class="absolute inset-0 flex items-center justify-center mt-10 pointer-events-none">
                    <span
                        class="text-4xl font-medium text-white animate-bounce drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)]">
                        -{{ damage }}
                    </span>
                </div>
            </div>
            <div
                class="col-span-7 bg-[#0a0a0a] rounded-3xl border border-gray-800 flex flex-col items-center justify-center p-12 relative">
                <Live @result="result_handle"></Live>
                <div class="h-3 w-10 border border-white/20">{{ result }} </div>
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
        <!-- <Trainer></Trainer>-->

        <!-- <div class="min-h-screen bg-slate-900 text-white flex flex-col items-center p-4 font-sans overflow-hidden"> -->

        <div class="w-full max-w-5xl m-auto mt-4 grid grid-cols-6">
            <div class="flex justify-between items-end mb-2">
                <span class="text-sm font-bold text-red-500">LV. {{ monster.level }}</span>
                <h2 class="text-xl font-black tracking-tighter">{{ monster.name }}</h2>
                <span class="text-sm text-gray-400">{{ monster.currentHp }}/{{ monster.maxHp }}</span>
            </div>

            <div
                class="w-full h-6 bg-gray-700 rounded-full border-2 border-gray-600 p-0.5 shadow-[0_0_15px_rgba(239,68,68,0.3)]">
                <div class="h-full bg-gradient-to-r from-orange-500 to-red-600 rounded-full transition-all duration-300 ease-out"
                    :style="{ width: (monster.currentHp / monster.maxHp * 100) + '%' }"></div>
            </div>
        </div>

        <!-- <div class="flex-1 w-full flex items-center justify-center relative">
            <transition-group name="damage">
                <div v-for="d in damageHistory" :key="d.id"
                    class="absolute text-3xl font-black text-yellow-400 z-10 italic pointer-events-none">
                    -{{ d.value }}
                </div>
            </transition-group>

            <div
                :class="['relative transition-transform', monster.currentHp <= 0 ? 'grayscale scale-75 opacity-50' : monster.animation]">
                <div
                    class="w-64 h-64 bg-gradient-to-b from-transparent to-red-900/20 rounded-full absolute -bottom-10 blur-2xl">
                </div>
            </div>
    </div> -->
    </div>



</template>
<script setup>
import Live from '../../Live/Live.vue';
import menu_btn from '../../../bases/menu_btn.vue';
import Trainer from '../../Trainer/Trainer.vue';
import { ref, computed, watch } from 'vue';
import { calculating, get_translate } from '../../../../composable/helpers';
const { from_left } = get_translate()
const { persen } = calculating()
// State của Quái vật
const oldValue = ref(0)
const result = ref()
const result_handle = (e) => {
    if (oldValue.value == e.total) {
        return;
    }
    result.value = e
    oldValue.value = e.total
    // console.log(e, typeof (e.total))
}
watch(result, (newValue) => {
    if (newValue.estimate == 'good') {

    }
})
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
const damage = 30
const show_damage = ref(false)
const handleHit = async () => {
    if (monster.value.currentHp > 0) {
        monster.value.currentHp -= damage;
        show_damage.value = true
        await new Promise(r => setTimeout(r, 500))
        show_damage.value = false

        if (monster.value.currentHp < 0) {
            monster.value.currentHp = 0
        }
    }
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
