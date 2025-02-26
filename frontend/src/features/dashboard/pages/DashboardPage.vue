<template>
	<v-row no-gutters
		><v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFirstAreaLoading"
					title="Опубликование всех нормативных правовых актов по годам"
				>
					<template #chart>
						<t-icon
							v-if="isFirstAreaLoading"
							name="dashboard"
							:width="80"
							:height="80"
						/>
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
					<!-- <template #previous>
						<v-btn
							color="primary"
							:loading="isFirstAreaPreviousLoading"
							@click="firstAreaPreviousYear"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isFirstAreaNextLoading"
							@click="firstAreaNextYear"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #interval v-if="!isThirdAreaLoading">
						{{ firstAreaYear.startDate }} -
						{{ firstAreaYear.endDate }}
					</template> -->
					<template #error> {{ firstAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isSecondAreaLoading"
					title="Опубликование всех типов нормативных правовых актов по месяцам"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isSecondAreaLoading"
						></t-skeleton-column-chart>

						<t-column-chart
							v-else
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
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="4">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isThirdAreaLoading"
					title="Опубликование по Федеральным округам по кварталам"
					:max-width="650"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isThirdAreaLoading"
						></t-skeleton-donut-chart>

						<t-donut-chart
							v-else
							:labels="thirdAreaLabels"
							:series="thirdAreaSeries"
							:is-legend-clickable="true"
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
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="4">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFourthAreaLoading"
					title="Опубликование по номенклатуре по годам"
					:max-width="650"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isFourthAreaLoading"
						></t-skeleton-donut-chart>
						<t-column-chart
							v-else
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
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="4">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFourthAreaLoading"
					title="Опубликование по Президенту по годам"
					:max-width="650"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isFourthAreaLoading"
						></t-skeleton-donut-chart>

						<t-donut-chart
							v-else
							:labels="fourthAreaLabels"
							:series="fourthAreaSeries"
							:height="350"
						/>
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
				</t-dashboard-area-card>
			</v-container>
		</v-col>

		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isSixthAreaLoading"
					title="Опубликование по ОГВ субъектов РФ минимальное за квартал"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isSixthAreaLoading"
						></t-skeleton-column-chart>

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
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFifthAreaLoading"
					title="Опубликование по ОГВ субъектов РФ максимальное за квартал"
				>
					<template #chart>
						<!-- <t-column-chart
							:labels="fifthAreaLabels"
							:series="fifthAreaSeries"
							:log-base="10"
							:enable-logarithmic="false"
							:y-start-value="0"
							:height="400"
						/> -->
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
				</t-dashboard-area-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import { TIcon } from '@/components/ui'
	import {
		TDashboardAreaCard,
		TDonutChart,
		THorizontalBarChart,
		TSkeletonDonutChart,
		TColumnChart,
		TSkeletonColumnChart,
	} from '../components/widgets'
	import {
		useChartArea,
		useFirstDashboardArea,
		useSecondDashboardArea,
		useThirdDashboardArea,
		useFifthDashboardArea,
		useSixthDashboardArea,
	} from '../composables'

	import { useDashboardStore } from '../store'
	import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils'
	import { computed } from 'vue'

	const store = useDashboardStore()

	const firstAreaLabels = computed(() => store.getPublicationByYearsLabels)
	const firstAreaSeries = computed(() => store.getPublicationByYearsSeries)
	const {
		error: firstAreaError,
		currentInterval: firstAreaYear,
		isPreviousLoading: isFirstAreaPreviousLoading,
		isNextLoading: isFirstAreaNextLoading,
		isDataLoading: isFirstAreaLoading,
		previousInterval: firstAreaPreviousYear,
		nextInterval: firstAreaNextYear,
	} = useChartArea({
		loadData: store.loadPublicationByYears,
		dropData: store.dropPublicationByYears,
		getInterval: getLastYear,
		interval: 'year',
	})

	const {
		secondAreaLabels,
		secondAreaSeries,
		secondAreaError,
		secondAreaDate,
		secondAreaMonth,
		isSecondAreaPreviousLoading,
		isSecondAreaNextLoading,
		isSecondAreaLoading,
		secondAreaPreviousMonth,
		secondAreaNextMonth,
	} = useSecondDashboardArea()

	const thirdAreaLabels = computed(
		() => store.getPublicationByDistrictsLabels,
	)
	const thirdAreaSeries = computed(
		() => store.getPublicationByDistrictsSeries,
	)

	const {
		error: thirdAreaError,
		currentInterval: thirdAreaQuarter,
		isPreviousLoading: isThirdAreaPreviousLoading,
		isNextLoading: isThirdAreaNextLoading,
		isDataLoading: isThirdAreaLoading,
		previousInterval: thirdAreaPreviousQuarter,
		nextInterval: thirdAreaNextQuarter,
	} = useChartArea({
		loadData: store.loadPublicationByDistricts,
		dropData: store.dropPublicationByDistricts,
		getInterval: getLastQuarter,
		interval: 'quarter',
	})

	const fourthAreaLabels = computed(
		() => store.getPublicationByNomenclatureLabels,
	)
	const fourthAreaSeries = computed(
		() => store.getPublicationByNomenclatureSeries,
	)
	const {
		error: fourthAreaError,
		currentInterval: fourthAreaYear,
		isPreviousLoading: isFourthAreaPreviousLoading,
		isNextLoading: isFourthAreaNextLoading,
		isDataLoading: isFourthAreaLoading,
		previousInterval: fourthAreaPreviousYear,
		nextInterval: fourthAreaNextYear,
	} = useChartArea({
		loadData: store.loadPublicationByNomenclature,
		dropData: store.dropPublicationByNomenclature,
		getInterval: getLastYear,
		interval: 'year',
	})

	const {
		fifthAreaLabels,
		fifthAreaSeries,
		fifthAreaError,
		fifthAreaDate,
		fifthAreaQuarter,
		isFifthAreaPreviousLoading,
		isFifthAreaNextLoading,
		isFifthAreaLoading,
		fifthAreaPreviousQuarter,
		fifthAreaNextQuarter,
	} = useFifthDashboardArea()
	const {
		sixthAreaLabels,
		sixthAreaSeries,
		sixthAreaError,
		sixthAreaDate,
		sixthAreaQuarter,
		isSixthAreaPreviousLoading,
		isSixthAreaNextLoading,
		isSixthAreaLoading,
		sixthAreaPreviousQuarter,
		sixthAreaNextQuarter,
	} = useSixthDashboardArea()
</script>

<style scoped></style>
