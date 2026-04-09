<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useExercise } from '../../../constants/exercise';
const { get_exercises } = useExercise()
const router = useRouter()
const attacks = ref(get_exercises())
// const attack = ref([
//   {
//     type: 'pushup',
//     name: 'Push-up',
//     emoji: '💪',
//     damage: 30,
//     bgColor: 'bg-linear-to-br from-blue-500 to-blue-700',
//     borderColor: 'border-blue-400',
//     tutorial: '/tutorial/pushup_tutorial',
//     description: 'Build upper body strength with classic push-ups!',
//     difficulty: 'Intermediate',
//     caloriesPerMin: 7,
//     muscle: 'Chest, Shoulders, Triceps'
//   },
//   {
//     id: 'squat',
//     name: 'Squat',
//     emoji: '🦵',
//     damage: 30,
//     bgColor: 'bg-linear-to-br from-purple-500 to-fuchsia-700',
//     borderColor: 'border-purple-400',
//     tutorial: '/tutorial/Squat Reach',
//     description: 'Strengthen your legs and core!',
//     difficulty: 'Beginner',
//     caloriesPerMin: 6,
//     muscle: 'Legs, Glutes, Core'
//   },
//   {
//     id: 'lungue',
//     name: 'Lungue',
//     emoji: '💪',
//     damage: 30,
//     bgColor: 'bg-linear-to-br from-cyan-500 to-blue-700',
//     borderColor: 'border-cyan-400',
//     tutorial: '/tutorial/Lunge',
//     description: 'Explosive leg power move!',
//     difficulty: 'Intermediate',
//     caloriesPerMin: 5,
//     muscle: 'Legs, Glutes, Balance'
//   },
//   {
//     id: 'bicep_curls',
//     name: 'Bicep Curls',
//     emoji: '☄️',
//     damage: 25,
//     bgColor: 'bg-linear-to-br from-orange-500 to-red-700',
//     borderColor: 'border-orange-400',
//     tutorial: '/tutorial/Bicep Curls',
//     description: 'Focus your power into your arms for a massive strike!',
//     difficulty: 'Beginner',
//     caloriesPerMin: 4,
//     muscle: 'Biceps, Forearms'
//   },
//   {
//     id: 'shoulder_press',
//     name: 'Shoulder Press',
//     emoji: '🌋',
//     damage: 45,
//     bgColor: 'bg-linear-to-br from-amber-500 to-yellow-700',
//     borderColor: 'border-amber-400',
//     tutorial: '/tutorial/Shoulder Press',
//     description: 'Crush your enemies by lifting the heavens!',
//     difficulty: 'Intermediate',
//     caloriesPerMin: 6,
//     muscle: 'Shoulders, Triceps'
//   },
// ]);

const current_exercise = ref('')

const emit = defineEmits(['send_current_exercise', 'is_analyst_active'])
const props = defineProps({
  start_analyst: Boolean
})

const handle_menu = () => {
  router.push({ name: 'menu' })
}

const handleSelectExercise = (attack) => {
  current_exercise.value = attack.type
  emit('send_current_exercise', attack)
}

// const getCurrentExerciseInfo = () => {
//   const exercise = attacks.value.find(a => a.id === current_exercise.value)
//   return exercise ? `${exercise.emoji} ${exercise.name}: ${exercise.description}` : ''
// }
</script>

<template>
  <div
    class="bg-gradient-to-t from-gray-900 via-gray-900/95 to-transparent backdrop-blur-sm border-t-2 border-emerald-500/50 shadow-2xl p-6">
    <div class="max-w-7xl m-auto">
      <!-- TITLE -->
      <div class="mb-6 text-center">
        <h2
          class="text-3xl font-black uppercase tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
          Chọn bài tập
        </h2>
        <p class="text-gray-400 text-sm mt-1">Chọn một bài tập và nhấn "start" để bắt đầu</p>
      </div>

      <!-- SKILLS GRID -->
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <button v-for="attack in attacks" :key="attack.type" @click="handleSelectExercise(attack)"
          :disabled="start_analyst"
          class="group relative p-4 rounded-2xl transition-all duration-300 transform overflow-hidden" :class="[
            attack.bgColor,
            attack.borderColor,
            'border-3 font-bold text-white',
            start_analyst && current_exercise !== attack.type
              ? 'opacity-30 grayscale blur-sm scale-95 cursor-not-allowed pointer-events-none'
              : 'hover:scale-105 active:scale-95',
            current_exercise === attack.type ? 'ring-4 ring-white scale-105 shadow-2xl' : ''
          ]">



          <!-- CONTENT -->
          <div class="relative z-10">
            <!-- EMOJI & NAME -->
            <div class="text-center mb-3">
              <div class="text-4xl mb-2">
                {{ attack.emoji }}
              </div>
              <h3 class="text-2xl font-black tracking-tight">
                {{ attack.type }}
              </h3>
            </div>

            <!-- DIFFICULTY BADGE -->
            <div class="flex justify-center mb-2">
              <span class="text-xs font-bold bg-white/20 px-2 py-1 rounded-full">
                {{ attack.difficulty }}
              </span>
            </div>

            <!-- STATS ROW -->
            <div class="grid grid-cols-2 gap-2 mb-3 text-xs font-semibold text-center">
              <div class="bg-black/40 rounded px-2 py-1">
                ⚡ {{ attack.damage }} DMG
              </div>
              <div class="bg-black/40 rounded px-2 py-1">
                🔥 {{ attack.kcal }}/{{ attack.time }} min
              </div>
            </div>
          </div>

          <!-- SELECTION INDICATOR -->
          <div v-if="current_exercise === attack.type"
            class="absolute top-2 right-2 bg-yellow-400 text-black px-3 py-1 rounded-full font-bold text-xs">
            ✓ READY
          </div>

          <!-- GLOW EFFECT WHEN SELECTED -->
          <div v-if="current_exercise === attack.type" class="absolute inset-0 rounded-2xl pointer-events-none"
            :class="'bg-white/30'"></div>
        </button>
      </div>

      <!-- BOTTOM ACTION - MENU BUTTON -->
      <div class="flex justify-center">
        <button @click="handle_menu"
          class="px-6 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 border-2 border-gray-600 text-white font-bold rounded-full transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg">
          ← Back to Menu
        </button>
      </div>
    </div>
  </div>
</template>
