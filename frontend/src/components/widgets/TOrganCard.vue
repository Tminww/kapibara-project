<template>
    <v-card
        class="mx-auto"
        :max-width="props.maxWidth"
        :min-width="props.minWidth"
        width="100%"
        elevation="3"
        :disabled="disabled"
    >
        <v-card-title>
            <div class="container">
                <t-icon :name="props.icon" :width="80" :height="80" />

                <div class="title-wrap">
                    {{ props.title }}
                </div>
            </div>
        </v-card-title>
        <v-card-text class="subtitle-wrap">
            {{ props.description }}
        </v-card-text>

        <v-card-text class="pb-0 pt-0">
            <slot name="chart"> </slot>
        </v-card-text>

        <v-card-actions>
            <div class="button-wrap">
                <v-btn color="primary" @click="goToNamedRouter" :disabled="disabled">
                    Перейти
                </v-btn>
            </div>
        </v-card-actions>
    </v-card>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { TIcon } from '@/components/ui'

const { disabled = false, ...props } = defineProps<{
    title: string
    description: string
    icon: string
    linkName: string
    maxWidth?: number
    minWidth?: number
    disabled?: boolean
}>()

const router = useRouter()

const goToNamedRouter = () => {
    router.push({ name: props.linkName })
}
</script>

<style scoped>
.title-wrap {
    white-space: normal; /* Позволяет перенос строк */
    word-wrap: break-word; /* Переносит слова, если они длинные */
    overflow-wrap: break-word;
    max-width: 100%; /* Ограничивает ширину заголовка */
    text-align: left; /* По желанию, можно выровнять текст */
    font-size: 18px;
    font-weight: bold;
}
.subtitle-wrap {
    white-space: normal; /* Позволяет перенос строк */
    word-wrap: break-word; /* Переносит слова, если они длинные */
    overflow-wrap: break-word;
    max-width: 100%; /* Ограничивает ширину заголовка */
    text-align: left; /* По желанию, можно выровнять текст */
    font-size: 14px;
    height: 80px;
    /* font-weight: bold; */
}
.button-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%; /* Или нужное значение */
}
.container {
    display: flex;
    align-items: center; /* Выравнивание элементов по центру */
    gap: 25px; /* Отступ между иконкой и текстом */
}
</style>
