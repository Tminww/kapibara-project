<template>
    <v-container>
        <v-row class="justify-space-around">
            <!-- Status Card -->
            <v-col cols="12" md="6">
                <StatusCard
                    title="Статус процесса проверки документов"
                    :status="status.state"
                    :message="status.status"
                    :progress="status.progress"
                    :isRunning="isRunning"
                    :startLoading
                    :startTime="status.startTime"
                    :endTime="status.endTime"
                    :duration="status.duration"
                    @start="showStartDialog"
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
                    description="Успешная проверка данных"
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
                                {{ item.report.summary?.processed || 0 }}
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
                            v-if="lastRun && lastRun.report && lastRun.report.details"
                            :headers="regionsHeaders"
                            :items="regionsItems"
                            density="compact"
                            fixed-header
                            fixed-footer
                            height="400"
                            v-model:sort-by="sortBy"
                            hover
                        >
                            <template v-slot:item.error="{ item }">
                                <v-checkbox-btn
                                    v-if="
                                        item.error === 'INVALID' && typeof item.reason === 'object'
                                    "
                                    v-model="item.reason.isValid"
                                    hide-details
                                    :true-value="true"
                                    :false-value="false"
                                    :disabled="true"
                                ></v-checkbox-btn>
                                <span v-else> Другое </span>
                            </template>
                            <template v-slot:item.state="{ item }">
                                <v-chip
                                    :color="getStateColor(item.state as string)"
                                    size="small"
                                    label
                                >
                                    {{ item.state }}
                                </v-chip>
                            </template>
                            <template v-slot:item.reason="{ item }">
                                {{ typeof item.reason === 'object' ? item.reason.similarity : 0 }}%
                            </template>
                            <template v-slot:item.="{ item }">
                                <v-checkbox-btn
                                    v-if="typeof item.reason === 'object'"
                                    v-model="item.reason.isValid"
                                    hide-details
                                    :true-value="true"
                                    :false-value="false"
                                    :disabled="true"
                                ></v-checkbox-btn>
                            </template>
                            <template #item.id="{ item }">
                                <v-btn
                                    class="text-none ma-1"
                                    prepend-icon="mdi-text-box-search"
                                    variant="text"
                                    @click="showCompareDialog(item)"
                                >
                                    Проверить
                                </v-btn>
                            </template>
                        </v-data-table>
                    </template>
                </ReportTableCard>
            </v-col>
        </v-row>

        <v-dialog v-model="startDialog" max-width="600">
            <v-card class="px-2 py-2">
                <v-card-title>Параметры проверки документов</v-card-title>
                <v-card-text class="py-2">
                    <v-form ref="validationForm" v-model="isFormValid">
                        <v-row>
                            <v-col cols="12" md="6">
                                <v-date-input
                                    v-model="validationParams.startDate"
                                    label="Начальная дата"
                                    :display-format="format"
                                    prepend-inner-icon="mdi-calendar-blank"
                                    prepend-icon=""
                                    variant="outlined"
                                    :rules="dateRules"
                                ></v-date-input>
                            </v-col>
                            <v-col cols="12" md="6">
                                <v-date-input
                                    v-model="validationParams.endDate"
                                    label="Конечная дата"
                                    :display-format="format"
                                    prepend-inner-icon="mdi-calendar-blank"
                                    prepend-icon=""
                                    variant="outlined"
                                    :rules="dateRules"
                                ></v-date-input>
                            </v-col>
                        </v-row>
                        <v-row class="mt-0 pt-0">
                            <v-col cols="12" class="my-0 py-0">
                                <v-checkbox
                                    v-model="validationParams.sendEmail"
                                    label="Отправить уведомление по email"
                                    hide-details
                                    density="compact"
                                ></v-checkbox>

                                <v-text-field
                                    v-if="validationParams.sendEmail"
                                    v-model="validationParams.recipientEmail"
                                    label="Email получателя"
                                    prepend-inner-icon="mdi-email-outline"
                                    variant="outlined"
                                    :rules="[rules.email]"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" variant="tonal" @click="startDialog = false">
                        Отменить
                    </v-btn>
                    <v-btn
                        color="success"
                        variant="tonal"
                        @click="startValidator"
                        :disabled="!isFormValid || startLoading"
                        :loading="startLoading"
                    >
                        Начать проверку
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Stop Confirmation Dialog -->
        <v-dialog v-model="stopDialog" max-width="500">
            <v-card class="px-2 py-2">
                <v-card-title> Подтвердите остановку </v-card-title>
                <v-card-text>
                    Вы уверены, что хотите <strong>остановить</strong> процесс валидации данных? Это
                    действие необратимо.
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" variant="tonal" @click="stopDialog = false">
                        Отменить
                    </v-btn>
                    <v-btn color="error" variant="tonal" @click="confirmStopValidator">
                        Остановить
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Compare Dialog -->
        <v-dialog v-model="compareDialog" max-width="800">
            <v-card class="px-2 py-2">
                <v-card-title>Сравнение текстов</v-card-title>
                <v-card-text class="px-2 py-2">
                    <v-row>
                        <v-col cols="6">
                            <v-card-subtitle>Текст из БД</v-card-subtitle>
                            <v-card-text class="bg-grey-lighten-4" style="white-space: pre-wrap">
                                {{ selectedItem?.reason.dbText }}
                            </v-card-text>
                        </v-col>
                        <v-col cols="6">
                            <v-card-subtitle>Текст из OCR</v-card-subtitle>
                            <v-card-text class="bg-grey-lighten-4" style="white-space: pre-wrap">
                                {{ selectedItem?.reason.ocrText }}
                            </v-card-text>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions class="gap-4">
                    <v-btn
                        color="success"
                        variant="tonal"
                        @click="validateDocument(selectedItem?.id, true)"
                        :loading="validationLoading"
                    >
                        Валиден
                    </v-btn>
                    <v-btn
                        color="error"
                        variant="tonal"
                        @click="validateDocument(selectedItem?.id, false)"
                        :loading="validationLoading"
                    >
                        Не валиден
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, shallowRef } from 'vue'
import { DateInstance, useDate } from 'vuetify'
import { VDateInput } from 'vuetify/lib/labs/VDateInput/index.mjs'
import { formatDate, formatDuration } from '@/utils/utils'
import { convertKeysFromSnakeToCamelCase } from '@/utils/caseConverter'
import api from '@/api'
import { default as StatsCard } from '@/shared/StatsCard.vue'
import { default as StatusCard } from '@/shared/StatusCard.vue'
import { default as HistoryTableCard } from '@/shared/HistoryTableCard.vue'
import { default as ReportTableCard } from '@/shared/ReportTableCard.vue'
import { toast } from 'vue-sonner'
import { send } from 'process'

interface Header {
    title: string
    key: string
    align: 'start' | 'center' | 'end'
    sortable: boolean
}

interface Reason {
    docExtId: string
    dbText: string
    ocrText: string
    similarity: number
    isValid: boolean
    status: string
}

interface Summary {
    total: number
    processed: number
    validationSuccessful: number
    validationFailed: number
    failed: number
    startDate: string
    endDate: string
    averageSimilarity: number
}
interface Detail {
    state: string
    error: number
    idReg: number
    idType: number
    reason: Reason | string
}

interface Report {
    details: Record<string, Detail>
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
        details: {},
        summary: {
            total: 0,
            processed: 0,
            validationSuccessful: 0,
            validationFailed: 0,
            failed: 0,
            startDate: '',
            endDate: '',
            averageSimilarity: 0.0
        }
    }
}

const rules = {
    required: (value: any) => !!value || 'Required.',
    counter: (value: any) => value.length <= 20 || 'Max 20 characters',
    email: (value: string) => {
        const pattern =
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Неверный e-mail.'
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
    { title: 'Обработано', key: 'summary', align: 'start', sortable: false },
    { title: 'Отчет', key: 'taskId', align: 'center', sortable: false }
]

// 2. Добавьте реализацию для regionsHeaders и regionsItems (перед компонентом v-data-table)
const regionsHeaders: Array<Partial<Header>> = [
    { title: 'Источник', key: 'idReg', align: 'start' },
    { title: 'Тип', key: 'idType', align: 'start' },
    { title: 'Состояние', key: 'state', align: 'start' },

    { title: 'Схожесть', key: 'reason', align: 'start' },
    { title: 'Валиден', key: 'error', align: 'start' },
    { title: 'Отчет', key: 'id', align: 'center' }
]

const regionsItems = computed(() => {
    if (!lastRun.value || !lastRun.value.report || !lastRun.value.report.details) {
        return []
    }
    return Object.entries(lastRun.value.report.details).map(([key, data]) => ({
        id: key,
        error: data.error || 'Unknown',
        idReg: data.idReg || 0,
        idType: data.idType || 0,
        reason: data.reason || ({} as Reason),
        state: data.state || 0
    }))
})

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
        name: 'Всего документов',
        value: lastRun.value.report?.summary?.total || 0,
        icon: 'mdi-file-document-outline'
    },
    {
        name: 'Обработано документов',
        value: lastRun.value.report?.summary?.processed || 0,
        icon: 'mdi-file-document-check-outline'
    },
    {
        name: 'Успешные проверки',
        value: lastRun.value.report?.summary?.validationSuccessful || 0,
        icon: 'mdi-check-circle-outline',
        color: 'success'
    },
    {
        name: 'Ошибки проверки',
        value: lastRun.value.report?.summary?.validationFailed || 0,
        icon: 'mdi-alert-circle-outline',
        color: 'error'
    },
    {
        name: 'Ошибки обработки',
        value: lastRun.value.report?.summary?.failed || 0,
        icon: 'mdi-alert-circle-outline',
        color: 'error'
    },
    {
        name: 'Процент схожести',
        value: lastRun.value.report?.summary?.averageSimilarity || 0,
        icon: 'mdi-percent-outline',
        color: 'gray'
    }
])

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
        const response = await api.validator.status()
        status.value = convertKeysFromSnakeToCamelCase(response)
        if (status.value.state === 'SUCCESS') {
            await fetchHistory()
            await fetchLastRun()
        }
    } catch (error) {
        console.error('Error fetching validator status:', error)
    } finally {
        loading.value = false
    }
}

const fetchHistory = async () => {
    try {
        loading.value = true
        const response = await api.validator.history({ limit: historyLimit.value })
        history.value = response.history
            ? response.history.map(convertKeysFromSnakeToCamelCase)
            : []

        if (history.value.length > 0 && !lastRun.value) {
            fetchLastRun()
        }
    } catch (error) {
        console.error('Error fetching validator history:', error)
    } finally {
        loading.value = false
    }
}

const fetchLastRun = async () => {
    try {
        const response = await api.validator.lastRun()
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

const startValidator = async () => {
    try {
        startLoading.value = true
        const params = {
            startDate: adapter
                .format(validationParams.value.startDate, 'YYYY-MM-DD')
                .toString()
                .split(',')[0],

            endDate: adapter
                .format(validationParams.value.endDate, 'YYYY-MM-DD')
                .toString()
                .split(',')[0],
            sendEmail: validationParams.value.sendEmail,
            recipientEmail: validationParams.value.recipientEmail
        }
        const response = await api.validator.start(params)
        console.log('Response from startValidator:', response)
        if (response.status === 200) {
            toast.success('Проверка данных запущена')
        }
        await new Promise((resolve) => setTimeout(resolve, 2000)) // Delay for 2 seconds

        await fetchStatus()
        await fetchHistory()
    } catch (error) {
        toast.error('Не удалось запустить процесс проверки данных')
    } finally {
        startLoading.value = false
        startDialog.value = false
    }
}
const showStartDialog = () => {
    startDialog.value = true
}

const showStopDialog = () => {
    console.log('showStopDialog')
    stopDialog.value = true
}

const confirmStopValidator = async () => {
    stopDialog.value = false

    try {
        await api.validator.stop()
        await fetchStatus()
        await fetchHistory()
    } catch (error) {
        console.error('Error stopping validator:', error)
    }
}

const setupStatusPolling = (): void => {
    statusInterval = setInterval(async () => {
        if (isRunning.value) {
            await fetchStatus()
        }
    }, 3000)
}

const startDialog = ref(false)
const isFormValid = ref(false)
const adapter = useDate()

interface ValidationParams {
    sendEmail: boolean
    recipientEmail: string
    startDate: DateInstance
    endDate: DateInstance
}

const format = (date: string) => {
    return adapter.toISO(date)
}
const validationParams = ref<ValidationParams>({
    sendEmail: false,
    recipientEmail: 'example@example.com',
    startDate: adapter.parseISO('2025-01-01') as DateInstance,
    endDate: adapter.parseISO('2025-01-01') as DateInstance
})

const dateRules = [(v: string) => !!v || 'Это поле обязательно']

// New state and methods for validation loading and compare dialog
const validationLoading = ref(false)
const compareDialog = ref(false)
const selectedItem = ref<{ id: string; reason: Reason } | null>(null)

const showCompareDialog = (item: any) => {
    selectedItem.value = item
    compareDialog.value = true
}

const validateDocument = async (id: string | undefined, isValid: boolean) => {
    if (!id) return

    try {
        validationLoading.value = true
        console.log({ id, is_valid: isValid })
        compareDialog.value = false
        // Optionally refresh data after validation
        await fetchHistory()
    } catch (error) {
        console.error('Error validating document:', error)
    } finally {
        validationLoading.value = false
    }
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
