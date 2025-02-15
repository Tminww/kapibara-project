<template>
	<!-- Фильтры в боковом меню -->
	<t-filter-sidebar
		v-model="leftMenu"
		:rail="rail"
		:loadingSubjects="loadingSubjects"
		:errorSubjects="errorSubjects"
		:districts="subjectStore.getRegionsToRequest"
		@update:rail="rail = $event"
	/>

	<v-container>
		<v-btn
			color="primary"
			variant="tonal"
			rounded
			@click="leftMenu = !leftMenu"
		>
			Фильтры
		</v-btn>

		<v-row no-gutters>
			<!-- Карточка с диаграммой (Опубликование по Федеральным округам) -->
			<v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isThirdAreaLoading"
						:min-width="500"
						:max-width="700"
						title="Опубликование по Федеральным округам"
					>
						<!-- <template #filter>
							<div class="button-group-wrap">
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый месяц</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый квартал</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый год</v-btn
								>
							</div></template
						> -->
						<template #chart>
							<t-skeleton-donut-chart v-if="isThirdAreaLoading" />
							<t-donut-chart
								v-else
								:labels="thirdAreaLabels"
								:series="thirdAreaSeries"
								:is-legend-clickable="true"
								:height="400"
							/>
						</template>
						<template #interval>
							<div v-if="!isThirdAreaLoading">
								{{ subjectStore.startDate }} -
								{{ subjectStore.endDate }}
							</div>
						</template>
						<template #error> {{ thirdAreaError }} </template>
					</t-dashboard-area-card>
				</v-container>
			</v-col>

			<!-- Карточка с диаграммой (Опубликование НПА по Федеральным округам) -->
			<v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isLogColumnChartLoading"
						:min-width="700"
						:max-width="700"
						title="Опубликование НПА по Федеральным округам"
					>
						<template #filter>
							<div class="button-group-wrap">
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый месяц</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый квартал</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый год</v-btn
								>
							</div></template
						>
						<template #chart>
							<t-skeleton-column-chart
								v-if="isLogColumnChartLoading"
							/>
							<t-column-chart
								v-else
								:labels="logColumnChartLabels"
								:series="logColumnChartSeries"
								:height="390"
							/>
						</template>
						<template #interval>
							<div v-if="!isLogColumnChartLoading">
								{{ subjectStore.startDate }} -
								{{ subjectStore.endDate }}
							</div>
						</template>
						<template #error> {{ logColumnChartError }} </template>
					</t-dashboard-area-card>
				</v-container>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue'
	import { TFilterSidebar } from '@/components/widgets'
	import { TDashboardAreaCard } from '@/components/widgets'
	import {
		TDonutChart,
		TSkeletonDonutChart,
		TColumnChart,
		TSkeletonColumnChart,
	} from '@/components/widgets'
	import { useSubjectStore } from '@/stores'
	import { useSubjectDashboardArea } from '@/composables/useSubjectDashboardArea'
	import { useLogColumnChart } from '@/composables/useLogColumnChart'

	// Состояния для загрузки фильтров
	const loadingSubjects = ref(false)
	const errorSubjects = ref(null)
	const leftMenu = ref(false)
	const rail = ref(false)

	const subjectStore = useSubjectStore()

	const loadSubjects = async () => {
		try {
			loadingSubjects.value = true
			errorSubjects.value = null
			await subjectStore.loadSubjectsAPI()
		} catch (e) {
			errorSubjects.value = e.message
			subjectStore.dropRegionsToRequest()
		} finally {
			loadingSubjects.value = false
		}
	}

	onMounted(async () => {
		await loadSubjects()
	})

	// Данные для первой карточки
	const {
		logColumnChartLabels,
		logColumnChartSeries,
		logColumnChartError,
		isLogColumnChartLoading,
	} = useLogColumnChart()

	// Данные для третьей карточки
	const {
		thirdAreaLabels,
		thirdAreaSeries,
		thirdAreaError,
		isThirdAreaLoading,
	} = useSubjectDashboardArea()
</script>

<style scoped>
	.button-group-wrap {
		display: flex;
		align-items: center; /* Выравнивание элементов по центру */
		gap: 5px; /* Отступ между иконкой и текстом */
	}
</style>
