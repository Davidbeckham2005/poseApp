<script setup>
import { computed, ref } from 'vue';
import { Camera } from 'lucide-vue-next'
// Mock Data
import { useUser } from '../../../store/user.store';
const userStore = useUser()

const user = ref({
    name: 'Alex Morgan',
    email: 'alex.morgan@email.com',
    joined: 'January 2025',
    level: 12,
    xp: 3450,
    nextLevelXp: 4000,
    streak: 7
});

const stats = computed(() => {
    return [
        { label: 'Total Sessions', value: userStore.user.total_session, icon: 'activity', color: 'text-cyan-400' },
        { label: 'Workout Time', value: userStore.user.total_time_work + "M", icon: 'clock', color: 'text-purple-400' },
        { label: 'Calories Burned', value: userStore.user.total_caloris, icon: 'zap', color: 'text-orange-400' },
        { label: 'Avg Accuracy', value: userStore.user.avg_accuracy + "%", icon: 'target', color: 'text-emerald-400' },
    ];
})
import { open } from "@tauri-apps/plugin-dialog";
import { convertFileSrc } from "@tauri-apps/api/core";

// component
import show_profile_value from './show_profile_value.vue';
import Profile_overview from './Profile_overview.vue';
import Profile_setting from './Profile_setting.vue';
import Profile_btn from './Profile_btn.vue';
import Achievement from './Achievement.vue';
import History from '../History/History.vue';
const avatar = ref()
async function change_avatar() {
    try {
        const pathSelected = await open({
            filters: [{
                name: "avatar",
                extensions: ["*"]
            }]
        })
        if (pathSelected) avatar.value = convertFileSrc(pathSelected)

    } catch (error) {
        console.log(error)
    }
}
const current_tab = ref('Overview')
const profile_tab = ['Overview', 'Achievement', 'Setting']
const switch_tab = (tab) => {
    current_tab.value = tab
}

</script>

<template>
    <div>
        <div class="mx-auto bg-gray-700/50 border border-white/20 rounded-3xl p-8">
            <div class="flex flex-col md:flex-row items-start md:items-center gap-6 mb-8 ">
                <div class="relative group">
                    <img :src="avatar" alt="Profile" 1
                        class="w-28 h-28 rounded-2xl object-cover border-2 border-slate-700" />
                    <div class="absolute -top-3 -right-3 bg-cyan-400 text-black font-bold px-2 py-1 rounded-lg text-sm">
                        LVL {{ user.level }}
                    </div>
                    <button @click="change_avatar"
                        class="absolute -bottom-2 -right-2 bg-cyan-400 p-2 rounded-full hover:bg-cyan-500 transition-colors text-black">
                        <Camera></Camera>
                    </button>
                </div>


                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <div>
                            <h1 class="text-3xl font-bold tracking-tight text-white">{{ userStore.user.name }}</h1>
                            <div class="flex gap-4 mt-1 text-slate-400 text-sm">
                                <span class="flex items-center gap-1"> {{ userStore.user.email }}</span>
                                <span class="flex items-center gap-1"> Joined {{ userStore.user.joined }}</span>
                            </div>
                        </div>
                        <Profile_btn @click="switch_tab('Setting')" text="Edit profile"></Profile_btn>

                    </div>

                    <div class="mt-6">
                        <div class="flex justify-between text-sm mb-2">
                            <span class="text-slate-400">Experience Points</span>
                            <span class="text-white">{{ user.xp }} / {{ user.nextLevelXp }} XP</span>
                        </div>
                        <div class="w-full h-3  rounded-full overflow-hidden">
                            <div class="h-full bg-cyan-400"
                                :style="{ width: (user.xp / user.nextLevelXp) * 100 + '%' }"></div>
                        </div>
                        <p class="text-[11px] text-slate-500 mt-2 uppercase tracking-wider">
                            {{ user.nextLevelXp - user.xp }} XP UNTIL LEVEL {{ user.level + 1 }}
                        </p>
                    </div>
                </div>

            </div>

            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <show_profile_value v-for="stat in stats" :stat="stat"></show_profile_value>
            </div>

            <!-- <div class="bg-orange-500/10 border border-orange-500/20 rounded-2xl p-4 flex items-center gap-4">
                <div class="bg-orange-500 p-3 rounded-xl shadow-lg shadow-orange-500/20">
                    🔥
                </div>
                <div>
                    <h3 class="font-bold text-orange-400 leading-tight">{{ user.streak }} Day Streak!</h3>
                    <p class="text-xs text-orange-300/70">Keep it up! You're on fire!</p>
                </div>
            </div> -->
        </div>
        <div>
            <div class="grid grid-2 lg:grid-cols-8">
                <div class="uppercase font-bold mt-8  pb-3  text-center"
                    :class="current_tab == tab ? 'text-cyan-400 border-b border-cyan-400' : 'border-b-gray-700/30 hover:border-cyan-400 border-b '"
                    v-for="tab in profile_tab" @click="switch_tab(tab)">{{
                        tab
                    }}
                </div>
            </div>
            <Profile_overview v-if="current_tab == 'Overview'" :stats="stats"></Profile_overview>
            <Profile_setting v-else-if="current_tab == 'Setting'" :user="userStore.user"></Profile_setting>
            <History v-else-if="current_tab == 'Achievement'">
            </History>
        </div>
    </div>
</template>