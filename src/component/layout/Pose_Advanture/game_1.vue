<script setup>
import { Sword, Shield, Zap } from 'lucide-vue-next';
import Trainer from '../Trainer/Trainer.vue'
import { useMonster, Use_is_warmup } from '../../../composable/help_game'
import menu_btn from '../../bases/menu_btn.vue';
const { get_all_monsters } = useMonster()
const monsters = get_all_monsters()
const { set_state_warmup } = Use_is_warmup()
const emit = defineEmits(['select']);
import { useRouter } from 'vue-router'
const router = useRouter()
const battle_handle = (key) => {
    console.log("Chiến đấu với:", key);
    set_state_warmup(true)
    router.push(`/game/battle/${key}`)
};
import Music from '../../bases/Music.vue'
</script>

<template>
    <div class="dark:bg-[#0a0a0a] text-white">
        <div class="h-15">
            <menu_btn></menu_btn>
            <Music></Music>
        </div>
        <div class="w-full max-w-6xl mx-auto p-6 ">
            <div class="mb-8 flex justify-between items-end px-4">
                <div>
                    <h1 class="text-white text-4xl font-black italic tracking-tighter uppercase">Chọn Đối Thủ</h1>
                    <p class="text-slate-400 font-medium">Chọn một quái vật để bắt đầu tập luyện</p>
                </div>
                <div class="text-slate-500 font-mono text-sm uppercase tracking-widest">
                    Total: {{ Object.keys(monsters).length }} Monsters
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                <div @click="battle_handle(key)" v-for="(monster, key) in monsters" :key="key" :class="[
                    monster.bg,
                    'group relative p-6 rounded-[2.5rem] cursor-pointer transition-all duration-500',
                    'hover:scale-[1.05] hover:shadow-[0_20px_50px_rgba(0,0,0,0.4)] shadow-xl overflow-hidden min-h-[320px] flex flex-col'
                ]">
                    <div
                        class="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    </div>

                    <div class="relative z-10 flex justify-between items-start mb-4">
                        <div
                            class="px-3 py-1 rounded-full text-[10px] font-black bg-black/20 text-white backdrop-blur-md border border-white/10 uppercase italic">
                            {{ monster.difficulty }}
                        </div>
                        <div
                            class="px-3 py-1 rounded-full text-[10px] font-black bg-yellow-400 text-black shadow-lg uppercase">
                            {{ monster.name }}
                        </div>
                    </div>

                    <div
                        class="relative z-10 flex-1 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-500">
                        <div class="w-full h-full min-h-[140px] flex items-center justify-center">
                            <Trainer :path_json="monster.path" :key="key"></Trainer>
                        </div>
                    </div>

                    <div class="relative z-10 mt-4 pt-4 border-t border-white/10">
                        <div class="flex items-center justify-between text-white">
                            <div class="flex flex-col">
                                <span class="text-[10px] font-bold opacity-70 uppercase tracking-tighter">Max HP</span>
                                <span class="text-2xl font-black italic tabular-nums leading-none">
                                    {{ monster.maxHp.toLocaleString() }}
                                </span>
                            </div>
                            <div
                                class="bg-white/20 p-2 rounded-xl group-hover:bg-white group-hover:text-black transition-colors">
                                <Sword :size="20" />
                            </div>
                        </div>
                    </div>

                    <div
                        class="absolute -top-[100%] -left-[100%] w-[200%] h-[200%] bg-gradient-to-br from-white/20 via-transparent to-transparent rotate-45 group-hover:top-[-50%] group-hover:left-[-50%] transition-all duration-1000 pointer-events-none">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Bo góc mượt mà cho các card */
.grid>div {
    backface-visibility: hidden;
}
</style>