<script setup>
import { ref } from 'vue';
const attacks = ref([
  {
    id: 'pushup',
    name: 'Push-up',
    damage: 50,
    bgColor: 'bg-gradient-to-br from-blue-400 to-blue-600',
    borderColor: 'border-blue-700',
    tutorial: '/tutorial/pushup_tutorial'
  },
  {
    id: 'squat',
    name: 'Squat',
    damage: 30,
    bgColor: 'bg-gradient-to-br from-purple-400 to-fuchsia-600',
    borderColor: 'border-purple-700',
    tutorial: '/tutorial/Squat Reach'
  },
  {
    id: 'lungue',
    name: 'Lungue',
    damage: 30,
    bgColor: 'bg-gradient-to-br from-purple-400 to-cyan-600',
    borderColor: 'border-purple-700',
    tutorial: '/tutorial/Lunge'

  },

]);


const current_exercise = ref('')
import { useRouter } from 'vue-router';
const router = useRouter()
const handle_menu = () => {
  router.push({ name: 'menu' })
}


const emit = defineEmits(['send_current_exercise'])
const props = defineProps({
  start_analyst: Boolean
})
</script>

<template>
  <div class="relative max-w-7xl space-y-3 w-full m-auto bg-gray-700/30 rounded-2xl p-4 border border-white/20">
    <div class="mb-2">
      <h2 class="text-xl font-medium uppercase mb-2">Chọn kỹ năng</h2>
    </div>
    <div class="grid grid-cols-2 lg:grid-cols-3 space-x-4 gap-2">
      <button :disabled="start_analyst" v-for="attack in attacks" :key="attack.name"
        @click="emit('send_current_exercise', attack, attack.tutorial), current_exercise = attack.id"
        class="p-2 group relative flex flex-col items-center justify-center rounded-2xl transition-all duration-150"
        :class="[attack.bgColor, attack.borderColor, start_analyst && current_exercise !== attack.id
          ? 'opacity-40 grayscale brightness-50 scale-95 pointer-events-none'
          : 'hover:scale-[1.02] active:scale-95 active:translate-y-0.5',]">

        <h3 class="mb-2 text-2xl font-medium tracking-tight text-white md:text-xl lg:text-2xl">
          {{ attack.name }}
        </h3>
        <div class="flex flex-col items-center gap-1.5 text-center text-white/90">
          <span class="text-xl font-medium tracking-tight">{{ attack.damage }} dmg</span>
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

  </div>
</template>
