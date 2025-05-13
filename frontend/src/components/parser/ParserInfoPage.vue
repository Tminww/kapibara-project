<template>
    <v-container>
        <v-row class="justify-space-around">
            <!-- Status Card -->
            <v-col cols="12" md="6">
                <StatusCard
                    title="Статус процесса сбора данных"
                    :status="status.state"
                    :message="status.status"
                    :progress="status.progress"
                    :isRunning="isRunning"
                    :startLoading
                    :startTime="status.startTime"
                    :endTime="status.endTime"
                    :duration="status.duration"
                    @start="startParser"
                    @confirm="showStopDialog"
                />
            </v-col>
            <!-- Performance Chart -->
            <v-col cols="12" md="6" v-if="hasHistoryData">
                <v-card class="h-100" elevation="3">
                    <v-card-title class="d-flex align-center">
                        <span>Длительность</span>
                        <v-spacer></v-spacer>
                        <v-select
                            v-model="historyLimit"
                            :items="[5, 10, 20, 50]"
                            variant="outlined"
                            density="compact"
                            hide-details
                            style="max-width: 120px"
                            @update:model-value="fetchHistory"
                            color="primary"
                        ></v-select>
                    </v-card-title>

                    <v-card-text>
                        <apexchart
                            type="area"
                            height="300"
                            :options="chartOptions"
                            :series="chartSeries"
                        ></apexchart>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Stats Cards -->
            <v-col cols="12" md="4" v-if="hasHistoryData">
                <StatsCard
                    color="success"
                    icon="check"
                    :amount="successfulRuns"
                    description="Успешный сбор данных"
                />
            </v-col>

            <v-col cols="12" md="4" v-if="hasHistoryData">
                <StatsCard
                    color="error"
                    icon="alert"
                    :amount="failedRuns"
                    description="Ошибки при выполнении"
                />
            </v-col>

            <v-col cols="12" md="4" v-if="hasHistoryData">
                <StatsCard
                    color="info"
                    icon="clock"
                    :amount="avgDuration"
                    description="Среднее время выполнения"
                />
            </v-col>

            <!-- History Table -->
            <v-col cols="12" :md="hasHistoryData ? 6 : 12">
                <HistoryTableCard historyLimit="20">
                    <template #table>
                        <v-data-table
                            :headers="historyHeaders"
                            :items="history"
                            :loading="loading"
                            items-per-page="15"
                            :items-per-page-options="[15, 20, 50]"
                            fixed-header
                            fixed-footer
                            height="700"
                            density="compact"
                            hover
                        >
                            <template v-slot:item.state="{ item }">
                                <v-chip :color="getStateColor(item.state)" size="small" label>
                                    {{ item.state }}
                                </v-chip>
                            </template>

                            <template v-slot:item.duration="{ item }">
                                {{ formatDuration(item.duration) }}
                            </template>

                            <template v-slot:item.startTime="{ item }">
                                {{ formatDate(item.startTime) }}
                            </template>
                            <template v-slot:item.summary="{ item }">
                                {{ item.report.summary.organsProcessed || 0 }}
                            </template>
                            <template #item.taskId="{ item }">
                                <v-btn
                                    class="text-none ma-1"
                                    prepend-icon="mdi-text-box-search"
                                    variant="text"
                                    @click="showReport(item.taskId)"
                                >
                                    Смотреть
                                </v-btn>
                            </template>
                        </v-data-table>
                    </template>
                </HistoryTableCard>
            </v-col>
            <!-- Last Report -->
            <v-col cols="12" md="6">
                <ReportTableCard
                    :status="lastRun.state"
                    :message="lastRun.status"
                    :stats="reportTableStats"
                >
                    <template #table>
                        <!-- Таблица регионов с результатами -->
                        <v-data-table
                            v-if="lastRun && lastRun.report && lastRun.report.organs"
                            :headers="regionsHeaders"
                            :items="regionsItems"
                            density="compact"
                            fixed-header
                            fixed-footer
                            height="400"
                            v-model:sort-by="sortBy"
                        >
                            <template v-slot:item.success="{ item }">
                                <v-chip color="success" size="small" label v-if="item.success > 0">
                                    {{ item.success }}
                                </v-chip>
                                <span v-else>{{ item.success }}</span>
                            </template>

                            <template v-slot:item.failed="{ item }">
                                <v-chip color="error" size="small" label v-if="item.failed > 0">
                                    {{ item.failed }}
                                </v-chip>
                                <span v-else>{{ item.failed }}</span>
                            </template>

                            <template v-slot:item.processed="{ item }">
                                <v-checkbox-btn
                                    v-model="item.processed"
                                    hide-details
                                    :true-value="true"
                                    :false-value="false"
                                    :disabled="true"
                                ></v-checkbox-btn>
                            </template>
                        </v-data-table>
                    </template>
                </ReportTableCard>
            </v-col>
        </v-row>

        <!-- Stop Confirmation Dialog -->
        <v-dialog v-model="stopDialog" max-width="500">
            <v-card class="px-2 py-2">
                <v-card-title class="text-h5"> Подтвердите остановку </v-card-title>
                <v-card-text>
                    Вы уверены, что хотите <strong>остановить</strong> процесс сбора данных? Это
                    действие необратимо.
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" variant="tonal" @click="stopDialog = false">
                        Отменить
                    </v-btn>
                    <v-btn color="error" variant="tonal" @click="confirmStopParser">
                        Остановить
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { formatDate, formatDuration } from '@/utils/utils'
import { convertKeysFromSnakeToCamelCase } from '@/utils/caseConverter'
import api from '@/api'
import { default as StatsCard } from '@/shared/StatsCard.vue'
import { default as StatusCard } from '@/shared/StatusCard.vue'
import { default as HistoryTableCard } from '@/shared/HistoryTableCard.vue'
import { default as ReportTableCard } from '@/shared/ReportTableCard.vue'

interface Header {
    title: string
    key: string
    align: 'start' | 'center' | 'end'
    sortable: boolean
}

interface Summary {
    organsProcessed: number
    organsTotal: number
    totalDocuments: number
    successful: number
    failed: number
    skipped: number
}
interface Organ {
    name: string
    total: number
    success: number
    failed: number
    skipped: number
    processed: boolean
}

interface Report {
    organs: Record<string, Organ>
    summary: Summary
}

interface Status {
    taskId: string
    state: 'SUCCESS' | 'FAILURE' | 'REVOKED' | 'STARTED' | 'PROGRESS' | 'UNKNOWN'
    status: string
    duration: number
    startTime: string
    endTime: string
    progress: number
    report: Report
}

// State
const defaultStatus: Status = {
    taskId: '',
    state: 'UNKNOWN',
    status: 'Загружаем информацию о сборе данных...',
    duration: 0,
    startTime: '',
    endTime: '',
    progress: 0,
    report: {
        organs: {},
        summary: {
            organsProcessed: 0,
            organsTotal: 0,
            totalDocuments: 0,
            successful: 0,
            failed: 0,
            skipped: 0
        }
    }
}
const status = ref<Status>({ ...defaultStatus })
const history = ref<Status[]>([])
const lastRun = ref<Status>({ ...defaultStatus })
const loading = ref(true)
const historyLimit = ref(50)
const stopDialog = ref(false)
const startLoading = ref(false)
const sortBy = [{ key: 'total', order: 'desc' as 'desc' | 'asc' }]
let statusInterval: NodeJS.Timeout

function showReport(taskId: string) {
    const foundItem = history.value.find((item) => item.taskId === taskId)
    lastRun.value = foundItem ? { ...foundItem } : { ...defaultStatus }
}

// History table setup
const historyHeaders: Array<Partial<Header>> = [
    { title: 'Статус', key: 'state', align: 'start', sortable: true },
    { title: 'Дата', key: 'startTime', sortable: true },
    { title: 'Длительность', key: 'duration', sortable: true },
    { title: 'Обработано', key: 'summary', align: 'center', sortable: false },
    { title: 'Отчет', key: 'taskId', align: 'center', sortable: false }
]

// 2. Добавьте реализацию для regionsHeaders и regionsItems (перед компонентом v-data-table)
const regionsHeaders: Array<Partial<Header>> = [
    { title: 'Источник', key: 'name', align: 'start' },
    { title: 'Код', key: 'code', align: 'start' },
    { title: 'Всего', key: 'total', align: 'start' },
    { title: 'Успешно', key: 'success', align: 'start' },
    { title: 'Ошибки', key: 'failed', align: 'start' },
    { title: 'Обработан', key: 'processed', align: 'center' }
]

const reportTableStats = computed(() => [
    {
        name: 'Начало',
        value: formatDate(lastRun.value.startTime),
        icon: 'mdi-clock-outline'
    },
    {
        name: 'Окончание',
        value: formatDate(lastRun.value.endTime),
        icon: 'mdi-clock-check-outline'
    },
    {
        name: 'Длительность',
        value: formatDuration(lastRun.value.duration),
        icon: 'mdi-timer-outline'
    },
    {
        name: 'Всего источников',
        value: lastRun.value.report.summary.organsTotal || 0,
        icon: 'mdi-database'
    },
    {
        name: 'Обработано источников',
        value: lastRun.value.report.summary.organsProcessed || 0,
        icon: 'mdi-database-check'
    },
    {
        name: 'Всего документов',
        value: lastRun.value.report.summary.totalDocuments || 0,
        icon: 'mdi-file-document-outline'
    },
    {
        name: 'Успешно',
        value: lastRun.value.report.summary.successful || 0,
        icon: 'mdi-check-circle-outline',
        color: 'success'
    },
    {
        name: 'Ошибки',
        value: lastRun.value.report.summary.failed || 0,
        icon: 'mdi-alert-circle-outline',
        color: 'error'
    },
    {
        name: 'Пропущено',
        value: lastRun.value.report.summary.skipped || 0,
        icon: 'mdi-help-circle-outline',
        color: 'gray'
    }
])
const regionsItems = computed(() => {
    if (!lastRun.value || !lastRun.value.report || !lastRun.value.report.organs) {
        return []
    }

    return Object.entries(lastRun.value.report.organs).map(([key, data]) => ({
        code: key,
        name: data.name || 'Unknown',
        total: data.total || 0,
        success: data.success || 0,
        failed: data.failed || 0,
        skipped: data.skipped || 0,
        processed: data.processed === true
    }))
})

// Computed properties
const isRunning = computed(() => {
    return status.value.state === 'STARTED' || status.value.state === 'PROGRESS'
})

// Chart data
const hasHistoryData = computed(() => {
    return history.value && history.value.length > 0
})

const chartSeries = computed(() => {
    // Only use entries with duration
    const entriesWithDuration = history.value
        .filter((entry) => entry.duration)
        .slice()
        .reverse()

    return [
        {
            name: 'Длительность',
            data: entriesWithDuration.map((entry) => entry.duration)
        }
    ]
})

const chartOptions = computed(() => {
    const entriesWithDuration = history.value
        .filter((entry) => entry.duration)
        .slice()
        .reverse()

    return {
        chart: {
            type: 'area',
            toolbar: {
                show: false
            },
            zoom: false,
            fontFamily: 'Nunito, sans-serif'
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        fill: {
            type: 'gradient',
            color: ['#'],
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.9,
                opacityTo: 0.5
            }
        },
        xaxis: {
            categories: entriesWithDuration.map((_, index) => `Запуск ${index + 1}`),
            labels: {
                // show: entriesWithDuration.length < 20 // Hide labels if too many data points
                show: false
            }
        },
        yaxis: {
            logarithmic: false,
            logBase: 10,
            labels: {
                show: true,
                formatter: function (value: number) {
                    return formatDuration(value)
                }
            },
            title: {
                show: false
            }
        },
        tooltip: {
            y: {
                formatter: function (value: number) {
                    return formatDuration(value)
                }
            }
        },
        theme: {
            mode: 'light',
            palette: 'palette1',
            monochrome: {
                enabled: true,
                color: '#1d4c86',
                shadeTo: 'light',
                shadeIntensity: 0.65
            }
        }
    }
})
const successfulRuns = computed((): number => {
    return history.value.filter((entry) => entry.state === 'SUCCESS').length
})

const failedRuns = computed((): number => {
    return history.value.filter((entry) => entry.state === 'FAILURE' || entry.state === 'REVOKED')
        .length
})

const avgDuration = computed(() => {
    const entriesWithDuration = history.value.filter((entry) => entry.duration)
    if (entriesWithDuration.length === 0) return '0 сек'

    const totalDuration = entriesWithDuration.reduce((sum, entry) => sum + entry.duration, 0)
    const avg = totalDuration / entriesWithDuration.length

    return formatDuration(avg)
})

// Methods
const getStateColor = (state: string) => {
    if (state === 'SUCCESS') return 'success'
    if (state === 'FAILURE' || state === 'REVOKED') return 'error'
    if (state === 'STARTED' || state === 'PROGRESS') return 'primary'
    return 'grey'
}

const fetchStatus = async () => {
    try {
        const response = await api.parser.status()
        status.value = convertKeysFromSnakeToCamelCase(response)
    } catch (error) {
        console.error('Error fetching parser status:', error)
    } finally {
        loading.value = false
    }
}

const fetchHistory = async () => {
    try {
        loading.value = true
        const response = await api.parser.history({ limit: historyLimit.value })
        history.value = response.history
            ? response.history.map(convertKeysFromSnakeToCamelCase)
            : []

        if (history.value.length > 0 && !lastRun.value) {
            fetchLastRun()
        }
    } catch (error) {
        console.error('Error fetching parser history:', error)
    } finally {
        loading.value = false
    }
}

const fetchLastRun = async () => {
    try {
        const response = await api.parser.lastRun()
        lastRun.value = convertKeysFromSnakeToCamelCase(response)
    } catch (error: any) {
        if (error.response && error.response.status === 404 && history.value.length > 0) {
            const sortedHistory = [...history.value].sort(
                (a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime()
            )
            if (sortedHistory[0] && sortedHistory[0].report) {
                lastRun.value = {
                    ...sortedHistory[0]
                }
            }
        } else if (error.response && error.response.status !== 404) {
            console.error('Error fetching last report:', error)
        }
    }
}

const startParser = async () => {
    try {
        startLoading.value = true
        await api.parser.start()
        await new Promise((resolve) => setTimeout(resolve, 2000)) // Delay for 2 seconds

        await fetchStatus()
        await fetchHistory()
    } catch (error) {
        console.error('Error starting parser:', error)
    } finally {
        startLoading.value = false
    }
}

const showStopDialog = () => {
    stopDialog.value = true
}

const confirmStopParser = async () => {
    stopDialog.value = false

    try {
        await api.parser.stop()
        await fetchStatus()
        await fetchHistory()
    } catch (error) {
        console.error('Error stopping parser:', error)
    }
}

const setupStatusPolling = (): void => {
    statusInterval = setInterval(async () => {
        if (isRunning.value) {
            await fetchStatus()
        }
    }, 3000)
}

// Lifecycle hooks
onMounted(async () => {
    await fetchStatus()
    await fetchHistory()
    await fetchLastRun()
    setupStatusPolling()
})

onUnmounted(() => {
    if (statusInterval) {
        clearInterval(statusInterval)
    }
})
</script>

<style scoped></style>
