<script setup lang="ts">
import { computed } from 'vue'
import { mapStatusToIcon, mapStatusToColor, formatDate, formatDuration } from '@/utils/utils'

interface Stat {
    icon: string
    name: string
    value: number | string
    color?: string
}
const props = defineProps<{
    status: 'SUCCESS' | 'FAILURE' | 'REVOKED' | 'STARTED' | 'PROGRESS' | 'UNKNOWN'
    message: string
    stats: Stat[]
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
    return 'mdi-information'
})
</script>

<template>
    <v-card class="h-100" elevation="3">
        <v-card-title class="d-flex align-center">
            <span>Отчет о выполнении</span>
            <v-spacer></v-spacer>
            <v-chip :color="statusColor" label class="ml-2">
                {{ status }}
            </v-chip>
        </v-card-title>
        <v-card-text class="pb-0">
            <v-alert
                :color="statusColor"
                :icon="statusIcon"
                variant="tonal"
                title="Статус выполнения"
                :text="message"
            >
            </v-alert>
            <!-- Статус выполнения -->
            <v-row no-gutters>
                <v-col cols="12" md="6">
                    <v-list density="compact">
                        <v-list-item
                            v-for="(stat, index) in stats.slice(0, Math.ceil(stats.length / 2))"
                            :key="stat.name"
                        >
                            <template v-slot:prepend>
                                <v-icon :icon="stat.icon"></v-icon>
                            </template>
                            <v-list-item-title>
                                {{ stat.name }}:
                                <v-chip v-if="stat.color" :color="stat.color" label>
                                    {{ stat.value }}
                                </v-chip>
                                <span v-else>{{ stat.value }}</span>
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-col>
                <v-col cols="12" md="6">
                    <v-list density="compact">
                        <v-list-item
                            v-for="(stat, index) in stats.slice(Math.ceil(stats.length / 2))"
                            :key="stat.name"
                        >
                            <template v-slot:prepend>
                                <v-icon :icon="stat.icon"></v-icon>
                            </template>
                            <v-list-item-title>
                                {{ stat.name }}:
                                <v-chip v-if="stat.color" :color="stat.color" label>
                                    {{ stat.value }}
                                </v-chip>
                                <span v-else>{{ stat.value }}</span>
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-col>
            </v-row>
            <slot name="table"> </slot>
        </v-card-text>
    </v-card>
</template>
