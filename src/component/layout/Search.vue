<!-- <template>
    <div class="relative">
        <Search class="absolute mt-3 ml-3"></Search>
        <input placeholder="Search by exercise name" type="text" class="block w-full pl-12 pr-4 py-3 bg-gray-700/50 border border-white/20 rounded-xl
            text-gray-300 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-cyan-400 focus:border-cyan-400
            transition-all" v-model="data_search">
    </div>
</template>
<script setup>
import { Search } from 'lucide-vue-next';
import { ref, watch } from 'vue';
const emit = defineEmits(['searchData'])
const data_search = ref()
watch(data_search, (newval) => {
    emit('searchData', newval)
})
</script> -->