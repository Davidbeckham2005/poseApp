<template>
    <div
        class="flex items-center justify-between p-4 bg-[#1a1a1e] hover:bg-[#252529] rounded-xl transition-all border border-white/5 cursor-pointer group">
        <div class="flex items-center gap-4">
            <div
                class="p-3 bg-slate-900 rounded-lg border border-orange-500/30 text-orange-400 group-hover:dark:bg-orange-500 group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                </svg>
            </div>
            <div>
                <h4 class="text-slate-100 font-bold tracking-tight">{{ activity.name }}</h4>
                <p class="text-xs text-slate-500 font-medium">{{ activity.date }}</p>
            </div>
        </div>

        <div class="flex items-center gap-6">
            <div class="text-right">
                <span class="block text-[10px] uppercase font-bold text-slate-500 tracking-wider">Reps</span>
                <span class="text-lg font-black text-white leading-tight">{{ activity.value }}</span>
            </div>
            <div class="px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-md">
                <span class="text-green-500 font-bold text-sm">{{ activity.accuracy }}%</span>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    activity: {
        type: Object,
        default: () => ({
            name: 'Squats',
            date: 'Today',
            value: 25,
            accuracy: 87
        })
    }
})
</script>