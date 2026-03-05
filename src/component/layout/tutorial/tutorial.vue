<script setup>
import { ref, computed } from 'vue';
import { Swords, Lightbulb, ChevronRight, ChevronLeft, BicepsFlexed, BowArrow, Shield, Flame, Activity, Trophy } from 'lucide-vue-next';
import Back_btn from '../../bases/Back_btn.vue'
const emit = defineEmits(['skip_tutorial'])
const handle_skip = () => {
    emit('skip_tutorial')
}
const totalSteps = 7
const currentStep = ref(1);
const Content = [
    {
        icon: Swords,
        title: 'Chào mừng, Chiến binh!',
        content:
            'Sân Đấu Thể Hình biến các bài tập ngoài đời thành trận chiến quái vật hoành tráng. Thực hiện động tác thật để tấn công kẻ địch, tạo combo và nâng cấp nhân vật!',
        tip: 'Bật webcam để nhận diện tư thế trực tiếp, hoặc chơi chế độ mô phỏng nếu không dùng camera.',
        background: 'bg-gradient-to-br from-blue-600 to-purple-700',
    },
    {
        icon: BicepsFlexed,
        title: 'Chọn Chiêu Thức',
        content:
            'Chọn 1 trong 3 bài tập: Chống đẩy, Squat, Plank. Mỗi động tác tiêu hao Thể lực và gây sát thương lên quái vật.',
        tip: 'Mỗi bài tập có lượng sát thương và tiêu hao thể lực khác nhau.',
        background: 'bg-gradient-to-br from-cyan-600 to-blue-700',
    },
    {
        icon: BowArrow,
        title: 'Độ Chuẩn Quan Trọng',
        content:
            'Tư thế của bạn được chấm điểm theo thời gian thực: - HOÀN HẢO — 1.5× sát thương, +1 combo - TỐT — 1.2× sát thương, +1 combo - SAI — sát thương thường, mất combo!',
        tip: 'Thực hiện động tác chậm và chuẩn để gây nhiều sát thương hơn.',
        background: 'bg-gradient-to-br from-green-600 to-emerald-700',
    },
    {
        icon: Flame,
        title: 'Hệ Thống Combo',
        content:
            'Chuỗi động tác Tốt hoặc Hoàn Hảo sẽ tăng combo. Khi đạt 5× combo, COMBO MODE kích hoạt và sát thương tăng mạnh. Sai tư thế sẽ mất toàn bộ combo!',
        tip: 'Luôn theo dõi thanh combo — sai một lần là mất hết.',
        background: 'bg-gradient-to-br from-orange-600 to-red-700',
    },
    {
        icon: Shield,
        title: 'Hiệu Ứng Trận Đấu',
        content:
            'Trước mỗi trận, bạn có thể chọn tối đa 2 hiệu ứng. thêm XP và phần thưởng lớn, hoặc tăng sát tương.',
        tip: 'Kết hợp nhiều hiệu ứng để thử thách bản thân và nhận thưởng tốt hơn.',
        background: 'bg-gradient-to-br from-purple-600 to-pink-700',
    },
    {
        icon: Activity,
        title: 'Khởi Động Trước Khi Chiến',
        content:
            'Mỗi trận đấu bắt đầu với khởi động ngắn: xoay cổ, xoay tay, xoay hông và chạy nhẹ. Hoàn thành sẽ nhận bonus trong 30 giây đầu.',
        tip: 'Bạn có thể bỏ qua, nhưng sẽ mất bonus và dễ chấn thương hơn.',
        background: 'bg-gradient-to-br from-teal-600 to-cyan-700',
    },
    {
        icon: Trophy,
        title: 'Sẵn Sàng Chiến Đấu!',
        content:
            'Hoàn thành nhiệm vụ hằng ngày để nhận XP, đánh bại quái vật để lên cấp và tiến hóa từ Tân Binh thành Huyền Thoại!',
        tip: 'Tiến độ nhiệm vụ sẽ được lưu giữa các trận đấu.',
        background: 'bg-gradient-to-br from-yellow-500 to-orange-600',
    },
];
const progressPercentage = computed(() => (currentStep.value / totalSteps) * 100);

const nextStep = () => {
    if (currentStep.value < totalSteps) currentStep.value++;
};

const prevStep = () => {
    if (currentStep.value > 1) currentStep.value--;
};
import { get_translate } from '../../../composable/helpers';
const { only_from_left } = get_translate()
</script>

<template>
    <div class="min-h-screen relative bg-black flex flex-col items-center justify-center p-4 font-sans text-white">
        <Back_btn></Back_btn>
        <div class="flex gap-2 mb-8">
            <div v-for="i in totalSteps" :key="i" :class="[
                'h-2.5 rounded-full transition-all duration-300',
                currentStep === i ? 'w-8 bg-orange-400' : 'w-2.5 bg-gray-600'
            ]"></div>
        </div>
        <Transition v-bind="only_from_left">
            <div class=" w-full max-w-2xl relative min-h-96 rounded-3xl p-12 text-center border border-white/10 overflow-hidden"
                :key="currentStep" :class="Content[currentStep - 1].background">
                <div class="flex flex-col items-center">
                    <div class="bg-white/10 p-4 rounded-2xl mb-6">
                        <component :is="Content[currentStep - 1].icon" :size="64" class="text-gray-200" />
                    </div>

                    <h1 class="text-4xl font-bold mb-4 tracking-tight">{{ Content[currentStep - 1].title }}</h1>

                    <p class="text-lg text-blue-100 leading-relaxed max-w-md">
                        {{ Content[currentStep - 1].content }}
                    </p>
                </div>
            </div>
        </Transition>
        <div
            class="w-full max-w-2xl mt-6 bg-orange-950/30 border border-orange-900/50 rounded-2xl p-4 flex items-start gap-3">
            <Lightbulb class="text-yellow-400 shrink-0" :size="20" />
            <p class="text-orange-200 text-sm">
                {{ Content[currentStep - 1].tip }}
            </p>
        </div>

        <div class="w-full max-w-2xl mt-8 flex items-center justify-between">
            <button @click="prevStep" :disabled="currentStep === 1"
                class="flex items-center gap-2 px-6 py-3 rounded-xl bg-gray-900 text-gray-500 font-semibold disabled:opacity-50 transition-colors hover:bg-gray-800">
                <ChevronLeft :size="20" />
                Trở lại
            </button>

            <button @click="handle_skip"
                class="text-gray-500 hover:text-white transition-colors underline underline-offset-4 text-sm font-medium">
                bỏ qua
            </button>

            <button @click="currentStep === 7 ? handle_skip() : nextStep()"
                :class="{ 'bg-gradient-to-br from-red-500 to-orange-700 text-white': currentStep === 7 }"
                class="flex items-center gap-2 px-10 py-3 rounded-2xl bg-orange-400 text-black font-bold hover:bg-orange-300 transition-all shadow-lg shadow-orange-500/20">
                {{ currentStep === 7 ? 'Bắt đầu ngay' : 'Tiếp theo' }}
                <ChevronRight :size="20" />
            </button>
        </div>

    </div>
</template>