<template>
    <tutorial v-if="get_state_tutorial()" @skip_tutorial="skip_tutorial"></tutorial>

    <div v-else>
        <div class="min-h-screen relative bg-[#0a0a0a] text-white p-6">
            <Back_btn></Back_btn>
            <menu_banner></menu_banner>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-full max-w-5xl mx-auto">
                <div v-for="(monster, key) in monsters" @click="battle_handle(key)"
                    :class="[monster.bg, 'group relative p-8 rounded-[2rem] cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl shadow-lg min-h-[180px]']">
                    <!-- <h2 class="text-2xl font-extrabold mb-1">{{ monster.maxHp }}</h2> -->
                    <div
                        class="absolute top-6 right-6 px-3 py-1 rounded-full text-[10px] font-black bg-yellow-400 text-black">
                        {{ monster.name }}
                    </div>

                    <div class="h-full flex flex-col justify-between">
                        <!-- <component :is="card.icon" :size="32" class="mb-4 text-white/90" /> -->
                        <!-- <div>
                            <h2 class="text-2xl font-extrabold mb-1">{{ card.title }}</h2>
                        </div> -->
                        <Trainer :path_json="monster.path"></Trainer>
                    </div>
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
const menuCards = [
    {
        // component: selectMonster,
        id: 'game1',
        title: 'Start Battle',
        desc: 'Fight monsters with real exercises',
        icon: Swords,
        bg: 'bg-gradient-to-br from-blue-500 to-cyan-400'
    },
];
</script>