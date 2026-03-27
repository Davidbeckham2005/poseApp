<template>
    <tutorial v-if="get_state_tutorial()" @skip_tutorial="skip_tutorial"></tutorial>

    <div v-else>
        <div class="min-h-screen relative dark:bg-[#0a0a0a] text-white p-6">
            <Back_btn></Back_btn>
            <menu_banner></menu_banner>
            <!-- <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-full max-w-5xl mx-auto">
                <div v-for="(monster, key) in monsters" @click="battle_handle(key)"
                    :class="[monster.bg, 'group relative p-8 rounded-[2rem] cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl shadow-lg min-h-[180px]']"> -->
            <!-- <h2 class="text-2xl font-extrabold mb-1">{{ monster.maxHp }}</h2> -->
            <!-- <div
                        class="absolute top-6 right-6 px-3 py-1 rounded-full text-[10px] font-black bg-yellow-400 text-black">
                        {{ monster.name }}
                    </div>

                    <div class="h-full flex flex-col justify-between"> -->
            <!-- <component :is="card.icon" :size="32" class="mb-4 text-white/90" /> -->
            <!-- <div>
                            <h2 class="text-2xl font-extrabold mb-1">{{ card.title }}</h2>
                        </div> -->
            <!-- <Trainer :path_json="monster.path"></Trainer>
                    </div>
                </div>
            </div> -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-5xl mx-auto">

                <div v-for="card in menuCards" :key="card.id" @click="handleSelect(card.id)" :class="[
                    'relative overflow-hidden cursor-pointer group rounded-3xl p-8 transition-all duration-500',
                    'bg-gradient-to-br shadow-2xl hover:scale-[1.02] hover:shadow-cyan-500/20',
                    card.bg]">
                    <div
                        class="absolute -inset-full bg-gradient-to-r from-transparent via-white/10 to-transparent rotate-45 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000">
                    </div>

                    <div class="relative z-10 flex flex-col gap-6">
                        <div class="flex justify-between items-start">
                            <div
                                class="p-4 bg-white/15 rounded-2xl backdrop-blur-lg border border-white/20 group-hover:rotate-6 transition-transform">
                                <component :is="card.icon" :size="40" color="white" stroke-width="2.5" />
                            </div>
                            <span
                                class="bg-black/20 text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-tighter">
                                Active Mode
                            </span>
                        </div>

                        <div>
                            <h2 class="text-3xl font-black text-white italic tracking-tight uppercase mb-2">
                                {{ card.title }}
                            </h2>
                            <p class="text-white/90 font-medium leading-relaxed max-w-[80%]">
                                {{ card.desc }}
                            </p>
                        </div>

                        <div
                            class="flex items-center gap-2 text-white font-bold text-sm mt-4 opacity-70 group-hover:opacity-100 transition-opacity">
                            CHƠI NGAY
                            <div
                                class="w-8 h-[2px] bg-white transform origin-left scale-x-50 group-hover:scale-x-100 transition-transform">
                            </div>
                        </div>
                    </div>

                    <component :is="card.icon"
                        class="absolute -bottom-6 -right-6 text-white/5 -rotate-12 scale-[3.0] transition-transform group-hover:scale-[3.5]" />
                </div>

            </div>
            <div class="mt-12 flex justify-center">
                <button @click="watch_tutorial"
                    class="flex items-center gap-2 text-gray-500 hover:text-white transition-colors text-sm font-bold uppercase tracking-widest">
                    <BookOpen :size="18" />
                    Hướng dẫn
                </button>
            </div>
        </div>

    </div>
</template>

<script setup>
import Trainer from '../Trainer/Trainer.vue'
import menu_banner from './menu_banner.vue'
import Back_btn from '../../bases/Back_btn.vue'
import tutorial from '../tutorial/tutorial.vue'
import { useRouter, useRoute } from 'vue-router'
import { Usetutorial } from '../../../composable/help_game'
import { useMonster, Use_is_warmup } from '../../../composable/help_game'
const { set_state_warmup } = Use_is_warmup()
const { get_all_monsters } = useMonster()
const { get_state_tutorial, set_state_tutorial } = Usetutorial()
const monsters = get_all_monsters()
const router = useRouter()
const current_game = ref('')

const handleSelect = (id) => {
    if (id === 'game1') {
        router.push('/game/game_1')
    } else if (id === 'game2') {
        router.push('/game/monster_selector')
    }
}
const skip_tutorial = () => {
    set_state_tutorial(false)
}
const watch_tutorial = () => {
    set_state_tutorial(true)

}

const battle_handle = (key) => {
    set_state_warmup(true)
    router.push(`/game/battle/${key}`)

}
import {
    Swords, Crown, Star, Trophy,
    Skull, Target, User, ChevronLeft,
    Settings, Play, BookOpen
} from 'lucide-vue-next';
import { ref } from 'vue'
const menuCards = [
    {
        // component: selectMonster,
        id: 'game1',
        title: 'Chế độ luyện tập',
        desc: 'Luyện tập với các bài tập thực tế',
        icon: Play,
        bg: 'bg-gradient-to-br from-blue-500 to-cyan-400'
    },
    {
        // component: selectMonster,
        id: 'game2',
        title: 'Chế độ chiến đấu',
        desc: 'Đánh bại quái vật với các bài tập thực tế',
        icon: Swords,
        bg: 'bg-gradient-to-br from-red-500 to-cyan-400'
    },
];
</script>