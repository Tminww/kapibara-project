<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { mapStatusToIcon, mapStatusToColor, formatDate, formatDuration } from '@/utils/utils'
const props = defineProps<{
    title: string
    status: 'SUCCESS' | 'FAILURE' | 'REVOKED' | 'STARTED' | 'PROGRESS' | 'UNKNOWN'
    message: string
    progress: number
    isRunning: boolean
    startLoading: boolean
    startTime: string
    endTime: string
    duration: number
}>()

const emit = defineEmits<{
    (e: 'start'): void
    (e: 'confirm'): void
}>()

const statusColor = computed(() => {
    if (mapStatusToColor[props.status]) {
        return mapStatusToColor[props.status]
    }
    return 'grey'
})

const statusIcon = computed(() => {
    if (mapStatusToIcon[props.status]) {
        return mapStatusToIcon[props.status]
    }
    return '    '
})

const startDuration = ref(0)
let durationInterval: NodeJS.Timeout

const currentDuration = computed(() => {
    if (!props.startTime) return 0
    if (props.endTime) {
        return props.duration || 0
    }
    return startDuration.value
})

// Функция для обновления значения duration
const updateDuration = () => {
    if (!props.startTime) return
    const startTime = new Date(props.startTime)
    const currentTime = new Date()
    startDuration.value = Math.floor((currentTime.getTime() - startTime.getTime()) / 1000)
}

// Настройка таймера для обновления duration
const setupDurationTimer = () => {
    // Остановить существующий таймер если есть
    if (durationInterval) {
        clearInterval(durationInterval)
    }

    // Запустить новый таймер только если процесс активен
    if (props.isRunning) {
        updateDuration() // Обновить сразу
        durationInterval = setInterval(updateDuration, 1000) // Обновлять каждую секунду
    }
}
// Следить за изменениями статуса для управления таймером
watch(
    () => props.status,
    (newValue, oldValue) => {
        if (newValue === 'STARTED' || newValue === 'PROGRESS') {
            setupDurationTimer()
        } else if (durationInterval) {
            clearInterval(durationInterval)
        }
    }
)

// Не забудьте очистить таймер при удалении компонента
onUnmounted(() => {
    if (durationInterval) {
        clearInterval(durationInterval)
    }
})
</script>

<template>
    <v-card class="d-flex flex-column" style="height: 100%" elevation="3">
        <v-card-title class="d-flex align-center">
            <span>{{ title }}</span>
            <v-spacer></v-spacer>
            <v-chip :color="statusColor" label class="ml-2">
                {{ status }}
            </v-chip>
        </v-card-title>

        <v-card-text class="flex-grow-1">
            <v-progress-linear
                v-if="isRunning"
                :model-value="progress"
                color="primary"
                height="25"
                rounded
                rounded-bar
            >
                <template v-slot:default="{ value }">
                    <strong
                        :style="{
                            color: Math.ceil(value) > 50 ? 'white' : 'black'
                        }"
                        >{{ Math.ceil(value) }}%</strong
                    >
                </template>
            </v-progress-linear>

            <v-alert
                :color="statusColor"
                :icon="statusIcon"
                variant="tonal"
                class="mt-2"
                title="Статус выполнения"
                :text="message"
            >
            </v-alert>

            <v-list v-if="startTime" density="compact">
                <v-list-item>
                    <template v-slot:prepend>
                        <v-icon icon="mdi-clock-start"></v-icon>
                    </template>
                    <v-list-item-title>Начало: {{ formatDate(startTime) }}</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="endTime">
                    <template v-slot:prepend>
                        <v-icon icon="mdi-clock-end"></v-icon>
                    </template>
                    <v-list-item-title>Окончание: {{ formatDate(endTime) }}</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="duration">
                    <template v-slot:prepend>
                        <v-icon icon="mdi-timer"></v-icon>
                    </template>
                    <v-list-item-title
                        >Длительность: {{ formatDuration(currentDuration) }}</v-list-item-title
                    >
                </v-list-item>
            </v-list>
        </v-card-text>

        <v-card-actions class="px-4 py-4">
            <v-btn
                :loading="startLoading"
                color="primary"
                @click="$emit('start')"
                :disabled="isRunning"
                prepend-icon="mdi-play"
                variant="tonal"
            >
                Начать
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
                color="error"
                @click="$emit('confirm')"
                :disabled="!isRunning"
                prepend-icon="mdi-stop"
                variant="tonal"
            >
                Остановить
            </v-btn>
        </v-card-actions>
    </v-card>
</template>
