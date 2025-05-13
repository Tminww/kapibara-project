<script setup>
import { iconValidator } from '@/utils/validators'
import { defineAsyncComponent, computed } from 'vue'

const props = defineProps({
    name: {
        type: String,
        required: true,
        validator: iconValidator
    },
    width: {
        type: [String, Number],
        default: 24 // Размер по умолчанию
    },
    height: {
        type: [String, Number],
        default: 24
    }
})

// Загружаем иконку асинхронно
const icon = defineAsyncComponent(() => import(`@/assets/icons/${props.name}.svg`))

// Преобразуем числа в строку с "px"
const iconWidth = computed(() =>
    typeof props.width === 'number' ? `${props.width}px` : props.width
)
const iconHeight = computed(() =>
    typeof props.height === 'number' ? `${props.height}px` : props.height
)
</script>

<template>
    <div class="container">
        <component :is="icon" :width="iconWidth" :height="iconHeight" />
    </div>
</template>

<style scoped></style>
