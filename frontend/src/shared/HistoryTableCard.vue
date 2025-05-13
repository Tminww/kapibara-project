<script setup lang="ts">
import { ref } from 'vue'

const { historyLimit = 20 } = defineProps<{
    historyLimit: number | string
}>()

const emit = defineEmits<{
    (e: 'update', limit: number): void
}>()

const slots = defineSlots<{
    table(): any
}>()

const currentHistoryLimit = ref(historyLimit)
</script>

<template>
    <v-card class="h-100" elevation="3">
        <v-card-title class="d-flex align-center">
            <span>История запусков</span>
            <v-spacer></v-spacer>
            <v-select
                v-model="currentHistoryLimit as number"
                :items="[5, 10, 20, 50]"
                variant="outlined"
                density="compact"
                hide-details
                :style="{ maxWidth: '120px' }"
                @update:model-value="$emit('update', currentHistoryLimit as number)"
                color="primary"
            ></v-select>
        </v-card-title>
        <v-card-text class="pb-0">
            <slot name="table"></slot>
        </v-card-text>
    </v-card>
</template>
