<template>
    <v-row no-gutters
        ><v-col cols="12" sm="12" md="12" lg="6" xl="6" xxl="6">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isFirstAreaLoading"
                    title="Опубликование всех НПА по годам"
                >
                    <template #chart>
                        <t-column-chart
                            v-if="!isFirstAreaLoading"
                            :labels="firstAreaLabels"
                            :series="firstAreaSeries"
                            :height="350"
                            :enable-logarithmic="false"
                            :log-base="10"
                            :y-start-value="0"
                        />
                    </template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="6" xl="6" xxl="6">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isSecondAreaLoading"
                    :title="
                        'Опубликование всех типов НПА за ' +
                        getMonthAndYearFromRuFormattedDate(secondAreaMonth.startDate)
                    "
                >
                    <template #chart>
                        <t-column-chart
                            :labels="secondAreaLabels"
                            :series="secondAreaSeries"
                            :height="350"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isSecondAreaPreviousLoading"
                            @click="secondAreaPreviousMonth"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isSecondAreaNextLoading"
                            @click="secondAreaNextMonth"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isSecondAreaLoading">
                        {{ secondAreaMonth.startDate }} -
                        {{ secondAreaMonth.endDate }}
                    </template>
                    <template #error> {{ secondAreaError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="4" xl="4" xxl="4">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isThirdAreaLoading"
                    title="Опубликование по всем ФО за квартал"
                    :is-title-clickable="true"
                    @onTitleClick="toRouteName('district')"
                >
                    <template #chart>
                        <t-donut-chart
                            :labels="thirdAreaLabels"
                            :series="thirdAreaSeries"
                            :is-legend-clickable="true"
                            legend-position="bottom"
                            :height="350"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isThirdAreaPreviousLoading"
                            @click="thirdAreaPreviousQuarter"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isThirdAreaNextLoading"
                            @click="thirdAreaNextQuarter"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isThirdAreaLoading">
                        {{ thirdAreaQuarter.startDate }} -
                        {{ thirdAreaQuarter.endDate }}
                    </template>
                    <template #error> {{ thirdAreaError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="4" xl="4" xxl="4">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isFourthAreaLoading"
                    :title="
                        'Опубликование по номенклатуре за ' +
                        fourthAreaYear.startDate.split('.')[2] +
                        ' г.'
                    "
                >
                    <template #chart>
                        <t-column-chart
                            :labels="fourthAreaLabels"
                            :series="fourthAreaSeries"
                            :height="350"
                        />
                        <!-- <t-donut-chart
							v-else
							:labels="fourthAreaLabels"
							:series="fourthAreaSeries"
							:height="350"
						/> -->
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isFourthAreaPreviousLoading"
                            @click="fourthAreaPreviousYear"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isFourthAreaNextLoading"
                            @click="fourthAreaNextYear"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isFourthAreaLoading">
                        {{ fourthAreaYear.startDate }} -
                        {{ fourthAreaYear.endDate }}
                    </template>
                    <template #error> {{ fourthAreaError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="4" xl="4" xxl="4">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isNomenclatureDetailLoading"
                    title="Детальное опубликование по номенклатуре за неделю"
                >
                    <template #chart>
                        <!-- <v-icon
							:loading="isNomenclatureDetailLoading"
							@click="copyNomenclatureDetail"
							size="16"
							>mdi-content-copy</v-icon
						> -->

                        <t-column-chart
                            :labels="nomenclatureDetailLabels"
                            :series="nomenclatureDetailSeries"
                            :height="350"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isNomenclatureDetailPreviousLoading"
                            @click="nomenclatureDetailPrevious"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isNomenclatureDetailNextLoading"
                            @click="nomenclatureDetailNext"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isNomenclatureDetailLoading">
                        {{ nomenclatureDetailInterval.startDate }} -
                        {{ nomenclatureDetailInterval.endDate }}
                    </template>
                    <template #error> {{ nomenclatureDetailError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="6" xl="6" xxl="6">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isFifthAreaLoading"
                    title="Минимальное опубликование по ОГВ субъектов РФ за квартал"
                >
                    <template #chart>
                        <t-horizontal-bar-chart
                            :labels="fifthAreaLabels"
                            :series="fifthAreaSeries"
                            :log-base="10"
                            :enable-logarithmic="false"
                            :y-start-value="0"
                            :height="350"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isFifthAreaPreviousLoading"
                            @click="fifthAreaPreviousQuarter"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isFifthAreaNextLoading"
                            @click="fifthAreaNextQuarter"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isFifthAreaLoading">
                        {{ fifthAreaQuarter.startDate }} -
                        {{ fifthAreaQuarter.endDate }}
                    </template>
                    <template #error> {{ fifthAreaError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="6" xl="6" xxl="6">
            <v-container :height="'100%'">
                <t-area-card
                    :isLoading="isSixthAreaLoading"
                    title="Максимальное опубликование по ОГВ субъектов РФ за квартал"
                >
                    <template #chart>
                        <t-horizontal-bar-chart
                            :labels="sixthAreaLabels"
                            :series="sixthAreaSeries"
                            :log-base="10"
                            :enable-logarithmic="false"
                            :y-start-value="0"
                            :height="350"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isSixthAreaPreviousLoading"
                            @click="sixthAreaPreviousQuarter"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next
                        ><v-btn
                            color="primary"
                            :loading="isSixthAreaNextLoading"
                            @click="sixthAreaNextQuarter"
                        >
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isSixthAreaLoading">
                        {{ sixthAreaQuarter.startDate }} -
                        {{ sixthAreaQuarter.endDate }}
                    </template>
                    <template #error> {{ sixthAreaError }}</template>
                </t-area-card>
            </v-container>
        </v-col>
    </v-row>
</template>

<script setup>
import { TAreaCard, TDonutChart, THorizontalBarChart, TColumnChart } from '../widgets'
import { useChartArea } from '../composables'

import { useDashboardStore } from '../stores/dashboard'
import { getLastMonth, getLastQuarter, getLastYear, getLastWeek } from '@/utils/utils'
import { computed } from 'vue'
import { toast } from 'vue-sonner'
import { useDate } from 'vuetify'
import { useRouter } from 'vue-router'

const getMonthAndYearFromRuFormattedDate = (currentDate) => {
    currentDate = currentDate.split('.').reverse().join('-')
    const date = useDate()

    return date.format(currentDate, 'monthAndYear')
}
const router = useRouter()
const store = useDashboardStore()

function toRouteName(routeName) {
    router.push({ name: routeName })
}
const copyNomenclatureDetail = () => {
    try {
        // Начало с общего количества
        let result = `Всего - ${store.getPublicationByNomenclatureDetailTotal}\n`

        // Маппинг имен из response к требуемым в образце
        const nameMapping = {
            'Федеральный конституционный закон': 'Федеральные конституционные законы',
            'Федеральный закон': 'Федеральные законы',
            'Указ Президента Российской Федерации': 'Указы президента Российской Федерации',
            'Распоряжение Президента Российской Федерации':
                'Распоряжения президента Российской Федерации',
            'Постановление Правительства Российской Федерации': 'Постановления правительства',
            'Распоряжение Правительства Российской Федерации': 'Распоряжения Правительства',
            'Конституционный Суд РФ': 'Постановления Конституционного суда',
            'Международные договоры РФ': 'Международные договоры Российской Федерации',
            'ФОИВ и ФГО РФ': 'Нормативные правовые акты федеральных органов исполнительной власти',
            'ОГВ Субъектов РФ': 'Правовые акты субъектов Российской Федерации'
        }

        // Фильтруем и форматируем строки
        const formattedStats = store.getPublicationByNomenclatureDetail
            .filter((item) => item.count > 0) // Пропускаем нулевые значения
            .map((item) => {
                const formattedName = nameMapping[item.name] || item.name // Используем маппинг или оригинальное имя
                return `${formattedName} – ${item.count}`
            })

        // Добавляем отфильтрованные строки к результату
        result += formattedStats.join('\n')
        navigator.clipboard.writeText(result)
        toast.success('Успешно скопировано!')
    } catch (err) {
        toast.error('Ошибка при копировании!')
    }
}
const firstAreaLabels = computed(() => store.getPublicationByYearsLabels)
const firstAreaSeries = computed(() => store.getPublicationByYearsSeries)
const {
    error: firstAreaError,
    currentInterval: firstAreaYear,
    isPreviousLoading: isFirstAreaPreviousLoading,
    isNextLoading: isFirstAreaNextLoading,
    isDataLoading: isFirstAreaLoading,
    previousInterval: firstAreaPreviousYear,
    nextInterval: firstAreaNextYear
} = useChartArea({
    loadData: store.loadPublicationByYears,
    dropData: store.dropPublicationByYears,
    getInterval: getLastYear,
    interval: 'year'
})

const secondAreaLabels = computed(() => store.getPublicationByTypesLabels)
const secondAreaSeries = computed(() => store.getPublicationByTypesSeries)
const {
    error: secondAreaError,
    currentInterval: secondAreaMonth,
    isPreviousLoading: isSecondAreaPreviousLoading,
    isNextLoading: isSecondAreaNextLoading,
    isDataLoading: isSecondAreaLoading,
    previousInterval: secondAreaPreviousMonth,
    nextInterval: secondAreaNextMonth
} = useChartArea({
    loadData: store.loadPublicationByTypes,
    dropData: store.dropPublicationByTypes,
    getInterval: getLastMonth,
    interval: 'month'
})

const thirdAreaLabels = computed(() => store.getPublicationByDistrictsLabels)
const thirdAreaSeries = computed(() => store.getPublicationByDistrictsSeries)

const {
    error: thirdAreaError,
    currentInterval: thirdAreaQuarter,
    isPreviousLoading: isThirdAreaPreviousLoading,
    isNextLoading: isThirdAreaNextLoading,
    isDataLoading: isThirdAreaLoading,
    previousInterval: thirdAreaPreviousQuarter,
    nextInterval: thirdAreaNextQuarter
} = useChartArea({
    loadData: store.loadPublicationByDistricts,
    dropData: store.dropPublicationByDistricts,
    getInterval: getLastQuarter,
    interval: 'quarter'
})

const fourthAreaLabels = computed(() => store.getPublicationByNomenclatureLabels)
const fourthAreaSeries = computed(() => store.getPublicationByNomenclatureSeries)
const {
    error: fourthAreaError,
    currentInterval: fourthAreaYear,
    isPreviousLoading: isFourthAreaPreviousLoading,
    isNextLoading: isFourthAreaNextLoading,
    isDataLoading: isFourthAreaLoading,
    previousInterval: fourthAreaPreviousYear,
    nextInterval: fourthAreaNextYear
} = useChartArea({
    loadData: store.loadPublicationByNomenclature,
    dropData: store.dropPublicationByNomenclature,
    getInterval: getLastYear,
    interval: 'year'
})

const nomenclatureDetailLabels = computed(() => store.getPublicationByNomenclatureDetailLabels)
const nomenclatureDetailSeries = computed(() => store.getPublicationByNomenclatureDetailSeries)
const {
    error: nomenclatureDetailError,
    currentInterval: nomenclatureDetailInterval,
    isPreviousLoading: isNomenclatureDetailPreviousLoading,
    isNextLoading: isNomenclatureDetailNextLoading,
    isDataLoading: isNomenclatureDetailLoading,
    previousInterval: nomenclatureDetailPrevious,
    nextInterval: nomenclatureDetailNext
} = useChartArea({
    loadData: store.loadPublicationByNomenclatureDetail,
    dropData: store.dropPublicationByNomenclatureDetail,
    getInterval: getLastWeek,
    interval: 'week'
})

const fifthAreaLabels = computed(() => store.getPublicationByRegionsMinLabels)
const fifthAreaSeries = computed(() => store.getPublicationByRegionsMinSeries)
const {
    error: fifthAreaError,
    currentInterval: fifthAreaQuarter,
    isPreviousLoading: isFifthAreaPreviousLoading,
    isNextLoading: isFifthAreaNextLoading,
    isDataLoading: isFifthAreaLoading,
    previousInterval: fifthAreaPreviousQuarter,
    nextInterval: fifthAreaNextQuarter
} = useChartArea({
    loadData: store.loadPublicationByRegionsMin,
    dropData: store.dropPublicationByRegionsMin,
    getInterval: getLastQuarter,
    interval: 'quarter'
})
const sixthAreaLabels = computed(() => store.getPublicationByRegionsMaxLabels)
const sixthAreaSeries = computed(() => store.getPublicationByRegionsMaxSeries)
const {
    error: sixthAreaError,
    currentInterval: sixthAreaQuarter,
    isPreviousLoading: isSixthAreaPreviousLoading,
    isNextLoading: isSixthAreaNextLoading,
    isDataLoading: isSixthAreaLoading,
    previousInterval: sixthAreaPreviousQuarter,
    nextInterval: sixthAreaNextQuarter
} = useChartArea({
    loadData: store.loadPublicationByRegionsMax,
    dropData: store.dropPublicationByRegionsMax,
    getInterval: getLastQuarter,
    interval: 'quarter'
})
</script>

<style scoped></style>
