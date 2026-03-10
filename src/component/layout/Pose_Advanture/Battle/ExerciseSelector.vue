<script setup>
import { ref } from 'vue';
const attacks = ref([
  {
    id: 'pushup',
    name: 'Push-up',
    damage: 50,
    bgColor: 'bg-gradient-to-br from-blue-400 to-blue-600',
    borderColor: 'border-blue-700'
  },
  {
    id: 'squat',
    name: 'Squat',
    damage: 30,
    bgColor: 'bg-gradient-to-br from-purple-400 to-fuchsia-600',
    borderColor: 'border-purple-700'
  },
  {
    id: 'lungue',
    name: 'Lungue',
    damage: 30,
    bgColor: 'bg-gradient-to-br from-purple-400 to-cyan-600',
    borderColor: 'border-purple-700'
  },
  // {
  //   id: 'plank',
  //   name: 'Plank',
  //   icon: '🛡️', // Shield icon to represent plank/defense
  //   energy: 20,
  //   damage: 15,
  //   bgColor: 'bg-gradient-to-br from-green-400 to-emerald-600',
  //   borderColor: 'border-green-700'
  // },
  // {
  //   id: 'jumpingjack',
  //   name: 'Jumping Jack',
  //   icon: '⚡', // Lightning bolt icon
  //   energy: 10,
  //   damage: 18,
  //   bgColor: 'bg-gradient-to-br from-amber-400 to-orange-500',
  //   borderColor: 'border-amber-700'
  // },
  // {
  //   id: 'lunge',
  //   name: 'Lunge',
  //   icon: '🏃', // Running man icon
  //   energy: 13,
  //   damage: 22,
  //   bgColor: 'bg-gradient-to-br from-rose-400 to-red-600',
  //   borderColor: 'border-rose-700'
  // }
]);


const current_exercise = ref('')
import { useRouter } from 'vue-router';
import { bool } from 'three/tsl';
const router = useRouter()
const handle_menu = () => {
  router.push({ name: 'menu' })
}

const openHelp = () => {
  console.log('Opening help...');
};
const emit = defineEmits(['send_current_exercise'])
const props = defineProps({
  start_analyst: Boolean
})
</script>

<template>
  <div class="relative max-w-6xl space-y-3 w-full m-auto bg-gray-700/30 rounded-2xl p-4 border border-white/20">
    <div class="mb-2">
      <h2 class="text-xl font-medium uppercase mb-2">Chọn kỹ năng</h2>
    </div>
    <div class="grid grid-cols-2 lg:grid-cols-5 space-x-4">
      <button :disabled="start_analyst" v-for="attack in attacks" :key="attack.name"
        @click="emit('send_current_exercise', attack), current_exercise = attack.id"
        class="p-2 group relative flex flex-col items-center justify-center rounded-2xl transition-all duration-150"
        :class="[attack.bgColor, attack.borderColor, start_analyst && current_exercise !== attack.id
          ? 'opacity-40 grayscale brightness-50 scale-95 pointer-events-none'
          : 'hover:scale-[1.02] active:scale-95 active:translate-y-0.5',]">
        <component :is="attack.icon" class=" text-6xl md:text-5xl lg:text-6xl">
        </component>

        <h3 class="mb-2 text-2xl font-medium tracking-tight text-white md:text-xl lg:text-2xl">
          {{ attack.name }}
        </h3>

        <div class="flex flex-col items-center gap-1.5 text-center text-white/90">
          <!-- <div cl ass="flex items-center gap-2"> -->
          <!-- <div
              class="flex h-7 w-7 items-center justify-center rounded-lg bg-black/15 border border-white/10 shadow-inner">
              <span class="text-lg">⚡</span>
            </div> -->
          <!-- <Zap :class="[attack.borderColor]"></Zap>
            <span class="text-xl font-medium">{{ attack.energy }}</span>
          </div> -->

          <span class="text-xl font-medium tracking-tight">{{ attack.damage }}<span
              class="font-normal opacity-90">dmg</span></span>
        </div>

        <div v-if="current_exercise === attack.id" class="absolute inset-0 rounded-3xl bg-black/20 ring-4 ring-white">
        </div>
      </button>
    </div>

    <div class="flex items-center justify-center">
      <button @click="handle_menu"
        class="flex items-center w-full rounded-2xl bg-gray-800/90 border border-white/20 py-2 text-xl font-medium transition-colors hover:bg-neutral-700 active:bg-neutral-800 active:scale-95 active:translate-y-0.5">
        <span class="text-2xl w-full text-center">←Quay lại menu</span>
      </button>
    </div>

    <button
      class="fixed bottom-6 right-6 flex h-14 w-14 items-center justify-center rounded-full bg-gray-800 text-3xl font-medium shadow-xl transition-all hover:bg-neutral-700 hover:text-white"
      aria-label="Help">
      ?
    </button>



  </div>
</template>

<style scoped>
/* Optional: prevent double-tap zoom on mobile buttons */
button {
  touch-action: manipulation;
}
</style>