<template>
    <div class="min-h-screen bg-slate-900 text-white pt-3">

        <menu_btn class="text-white"></menu_btn>
        <Warmup v-if="get_state_warmup()"></Warmup>
        <div v-else>
            <div class="max-w-6xl m-auto grid grid-cols-12 mb-4 gap-4">
                <div class="col-span-5 rounded-3xl border relative border-red-800  flex flex-col overflow-hidden p-5">
                    <!-- <div class="p-6 text-center">
                    <h2 class="text-2xl font-bold tracking-tight">{{ monster.name }}</h2>
                    <p class="text-gray-500 text-sm font-medium">Level {{ monster.level }} · ATK {{ monster.atk }}
                    </p>
                </div> -->

                    <div class="rounded-3xl" :class="{
                        [monster.bg]: hpPercentage >= 75,
                        'bg-orange-400/30': hpPercentage < 75 && hpPercentage >= 25,
                        'bg-red-600/70 animate-pulse': hpPercentage <= 25 && hpPercentage > 0,
                        'animate-shake border-red-500/70 border-2': show_damage,
                        'animate-death': monster.currentHp == 0
                    }">
                        <div class="w-[70%] max-w-6xl m-auto">
                            <div class="flex justify-between items-end mb-0.5">
                                <!-- <span class="text-sm font-bold text-red-500">LV. {{ monster.level }}</span> -->
                                <h2 class="text-xl font-black tracking-tighter">{{ monster.name }}</h2>
                                <span class="px-3 py-1 rounded-full text-[10px] font-black bg-yellow-400 text-black">HP
                                    {{ monster.currentHp }}/{{ monster.maxHp
                                    }}</span>
                            </div>

                            <div class="max-w-3xl w-full h-6 bg-gray-700 rounded-full border-2 border-gray-600 p-0.5">
                                <div class="h-full bg-gradient-to-r from-orange-500 to-red-600 rounded-full"
                                    :style="{ width: (monster.currentHp / monster.maxHp * 100) + '%' }"></div>
                            </div>
                        </div>
                        <Trainer :path_json="monster.path">
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
                </div>
            </div>
            <ExerciseSelector @send_current_exercise="handle_current_exercise_type" :start_analyst="is_start">
            </ExerciseSelector>
        </div>
    </div>
</template>
<script setup>
import ExerciseSelector from './ExerciseSelector.vue';
import Live from '../../Live/Live.vue';
import menu_btn from '../../../bases/menu_btn.vue';
import Trainer from '../../Trainer/Trainer.vue';
import { ref, computed, watch } from 'vue';
import { calculating, get_translate } from '../../../../composable/helpers';
import Warmup from '../Warmup.vue';
import { Use_is_warmup } from '../../../../composable/help_game';
const { get_state_warmup } = Use_is_warmup()
import { useMonster } from '../../../../composable/help_game';
// import { useRoute } from 'vue-router';
// const route = useRoute()
// console.log(route.params.monster)
const { get_monster } = useMonster()
const { persen } = calculating()
console.log(get_state_warmup())
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


const monster = computed(() => get_monster())
const stats = ref({
    hp: 94,
    maxHp: 100,
    stamina: 100,
    maxStamina: 100,
    combo: 0
});

watch(monster.value.currentHp, (newValue) => {
    if (newValue) {
        alert("victory!")
    }
})
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
