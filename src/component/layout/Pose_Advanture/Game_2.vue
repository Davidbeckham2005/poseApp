<template>
    <div class="min-h-screen overflow-hidden bg-[#050816] text-white relative">
        <div class="w-full h-15">
            <Back_btn></Back_btn>
            <!-- <Music></Music> -->
        </div>
        <!-- <div class="absolute inset-0 pointer-events-none">
            <div class="absolute -top-32 -left-32 h-80 w-80 rounded-full bg-cyan-500/20 blur-3xl"></div>
            <div class="absolute top-1/3 -right-24 h-96 w-96 rounded-full bg-orange-500/20 blur-3xl"></div>
            <div class="absolute bottom-0 left-1/4 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl"></div>
        </div> -->

        <div class="relative mx-auto max-w-7xl px-4 py-6 lg:px-8 lg:py-8">
            <div class="mb-6 flex items-center justify-between gap-4">
                <div class="">
                    <p class="text-xs uppercase tracking-[0.35em] text-cyan-300/80">Workout Builder</p>
                    <h1 class="text-3xl font-black tracking-tight sm:text-4xl">Choose your game mode</h1>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
                <section
                    class="overflow-hidden rounded-4xl border border-white/10 bg-white/5 p-5 shadow-2xl backdrop-blur-xl lg:p-6">
                    <div class="mt-6 rounded-3xl border border-white/10 bg-black/20 p-5">
                        <div class="flex items-center justify-between gap-4">
                            <div>
                                <p class="text-xs font-bold uppercase tracking-[0.3em] text-orange-300/80">Summary</p>
                                <h3 class="mt-1 text-lg font-black">{{ enabledCount }} exercises ready</h3>
                            </div>
                            <button @click="resetPlan"
                                class="inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-sm font-semibold text-white/80 transition hover:bg-white/10 hover:text-white">
                                <RotateCcw :size="16" />
                                Reset
                            </button>
                        </div>

                        <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                            <div class="rounded-2xl bg-white/5 p-3">
                                <p class="text-[10px] uppercase tracking-[0.25em] text-white/50">Total target</p>
                                <p class="mt-1 text-2xl font-black">{{ totalTarget }}</p>
                            </div>
                            <div class="rounded-2xl bg-white/5 p-3">
                                <p class="text-[10px] uppercase tracking-[0.25em] text-white/50">Mode</p>
                                <p class="mt-1 text-lg font-black capitalize">{{ selectedMode }}</p>
                            </div>
                            <div class="rounded-2xl bg-white/5 p-3">
                                <p class="text-[10px] uppercase tracking-[0.25em] text-white/50">Game side</p>
                                <p class="mt-1 text-lg font-black">Monster</p>
                                <p class="mt-1 text-lg text-red-500 font-black">{{ totalDamage }}HP</p>
                            </div>
                            <div class="rounded-2xl bg-white/5 p-3">
                                <p class="text-[10px] uppercase tracking-[0.25em] text-white/50">Plan</p>
                                <p class="mt-1 text-lg font-black">Custom</p>
                            </div>
                        </div>

                        <div class="mt-5 flex gap-3">
                            <button @click="enableAll"
                                class="flex-1 rounded-2xl border border-cyan-400/30 bg-cyan-400/10 px-4 py-3 text-sm font-bold text-cyan-100 transition hover:bg-cyan-400/20">
                                Select all
                            </button>
                            <button @click="clearAll"
                                class="flex-1 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-bold text-white/80 transition">
                                Clear all
                            </button>
                        </div>

                        <button @click="startWorkout"
                            class="mt-5 w-full rounded-2xl bg-linear-to-r from-emerald-400 to-cyan-400 px-5 py-4 text-base font-black uppercase tracking-[0.2em] text-slate-950 transition hover:scale-[1.01] active:scale-[0.99]">
                            Bắt đầu
                        </button>
                    </div>
                </section>

                <section class="rounded-4xl border border-white/10 bg-white/5 p-5 shadow-2xl backdrop-blur-xl lg:p-6">
                    <div class="mb-5 flex items-center justify-between gap-4">
                        <div>
                            <p class="text-xs font-bold uppercase tracking-[0.3em] text-emerald-300/80">Exercises</p>
                            <h2 class="mt-1 text-2xl font-black">Set reps for each move</h2>
                        </div>
                        <ListChecks class="text-emerald-300" :size="28" />
                    </div>

                    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
                        <article v-for="exercise in workoutItems" :key="exercise.type"
                            class="rounded-3xl border p-4 transition"
                            :class="exercise.enabled ? 'border-white/15 bg-black/20' : 'border-white/5 bg-white/5 opacity-60'">
                            <div class="flex items-start justify-between gap-3">
                                <div>
                                    <div class="flex items-center gap-2">
                                        <h3 class="text-lg font-black">{{ exercise.title }}</h3>
                                        <span
                                            class="rounded-full bg-white/10 px-2 py-1 text-[10px] font-bold uppercase tracking-[0.2em] text-white/70">
                                            {{ exercise.difficulty }}
                                        </span>
                                    </div>
                                    <p class="mt-2 max-w-md text-sm leading-relaxed text-white/65">
                                        {{ exercise.description }}
                                    </p>
                                </div>

                                <label
                                    class="inline-flex cursor-pointer items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-white/70">
                                    <input v-model="exercise.enabled" type="checkbox"
                                        class="h-4 w-4 rounded border-white/20 bg-transparent text-cyan-400 focus:ring-cyan-400" />
                                    Active
                                </label>
                            </div>

                            <div class="mt-4 grid gap-4 sm:grid-cols-[1fr_auto]">
                                <div>
                                    <div
                                        class="flex items-center justify-between text-xs font-bold uppercase tracking-[0.2em] text-white/50">
                                        <span>Target reps</span>
                                        <span>{{ exercise.target }} reps</span>
                                    </div>
                                    <input v-model.number="exercise.target" type="range" min="3" max="30" step="1"
                                        class="mt-3 h-2 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-cyan-400" />
                                </div>
                                <div class="flex items-center gap-2">
                                    <div class="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-center">
                                        <p class="text-[10px] uppercase tracking-[0.2em] text-white/40">Damage</p>
                                        <p class="text-lg font-black">{{ exercise.damage }}</p>
                                    </div>
                                    <input v-model.number="exercise.target" type="number" min="3" max="30"
                                        class="w-24 rounded-2xl border border-white/10 bg-black/30 px-3 py-3 text-center text-lg font-black outline-none transition focus:border-cyan-400" />
                                </div>
                            </div>
                        </article>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useExercise } from '../../../constants/exercise'
import { useGameChoose } from '../../../composable/help_game'
import { ArrowLeft, ListChecks, Play, RotateCcw, Shield, Swords } from 'lucide-vue-next'
import Back_btn from '../../bases/Back_btn.vue'
const router = useRouter()
const { get_exercises } = useExercise()
const { set_game_choose } = useGameChoose()

const defaultTargets = {
    squat: 12,
    pushup: 10,
    plank: 20,
    lungue: 10,
    bicep_curls: 8,
    shoulder_press: 10,
}

const buildWorkoutItems = () => get_exercises().map((exercise) => ({
    type: exercise.type,
    title: exercise.title,
    description: exercise.description,
    difficulty: exercise.difficulty,
    damage: exercise.damage ?? exercise.damege ?? 0,
    enabled: true,
    target: defaultTargets[exercise.type] || 10,
}))

const workoutItems = ref(buildWorkoutItems())
const selectedMode = ref('battle')



const enabledExercises = computed(() => workoutItems.value.filter((exercise) => exercise.enabled && exercise.target > 0))
const enabledCount = computed(() => enabledExercises.value.length)
const totalTarget = computed(() => enabledExercises.value.reduce((sum, exercise) => sum + Number(exercise.target || 0), 0))
const totalDamage = computed(() => enabledExercises.value.reduce((sum, exercise) => sum + Number(exercise.damage || 0) * Number(exercise.target), 0))
const enableAll = () => {
    workoutItems.value.forEach((exercise) => {
        exercise.enabled = true
    })
}

const clearAll = () => {
    workoutItems.value.forEach((exercise) => {
        exercise.enabled = false
    })
}

const resetPlan = () => {
    workoutItems.value = buildWorkoutItems()
    selectedMode.value = 'battle'
}

const startWorkout = () => {
    const plan = enabledExercises.value.map((exercise) => ({
        type: exercise.type,
        target: Number(exercise.target),
        title: exercise.title,
        damage: exercise.damage,
    }))

    if (!plan.length) {
        alert('Please choose at least one exercise.')
        return
    }

    set_game_choose('game2')
    router.push({
        name: 'game_2_battle',
        query: {
            mode: selectedMode.value,
            plan: JSON.stringify(plan),
            hp: totalDamage.value + totalDamage.value,
        },
    })
}
</script>
