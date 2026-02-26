<template>
    <div class="flex flex-row justify-between hover:bg-gray-700/80 p-2 rounded-2xl" @click="show_result(output_path)">
        <div class="flex flex-row space-x-2">
            <div class="rounded-md flex px-3 items-center bg-stone-900/70">
                <FileCheckCornerIcon class="h-6 w-6"></FileCheckCornerIcon>
            </div>
            <div>
                <p class="text-md font-semibold">{{ output_path }}</p>
                <p class="text-gray-500 text-sm">{{ size_video }}</p>
            </div>
        </div>
        <div class="flex space-x-2">
            <div class="flex flex-col font-semibold text-sm mr-2">
                <span class="">count</span>
                <span class="text-cyan-400 text-sm">{{ count }}</span>
            </div>
            <div class="flex flex-col font-semibold text-sm">
                <span>Score</span>
                <span :class="{
                    'text-green-400': accuracy_good > 65,
                    'text-orange-400': accuracy_good <= 65 && accuracy_good > 0,
                    'text-red-400': accuracy_good == 0
                }">{{ accuracy_good }}%</span>
            </div>
        </div>
    </div>
    <div>

    </div>
</template>

<script setup>
import { FileCheckCorner, FileCheckCornerIcon } from 'lucide-vue-next'
import { useNavigation } from '../../../composable/helpers';
const { switch_dashbroad } = useNavigation()
defineProps({
    count: Number,
    count_good: Number,
    accuracy_good: Number,
    output_path: String,
    size_video: String,
})
const show_result = (output_path) => {
    switch_dashbroad(output_path)
}
</script>