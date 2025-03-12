<template>
	<!-- Фильтры в боковом меню -->
	<t-filter-sidebar
		v-model="leftMenu"
		:rail="rail"
		:loadingSubjects="loadingSubjects"
		:errorSubjects="errorSubjects"
		:regions="store.getSubjects"
		@update:rail="rail = $event"
	/>

	<div class="flex justify-end">
		<v-btn
			class="my-4 ml-4 mr-4"
			color="primary"
			variant="tonal"
			@click="leftMenu = !leftMenu"
		>
			Фильтры
		</v-btn>
	</div>

	<v-row no-gutters class="justify-space-around">
		<v-col cols="auto">
			<v-container>
				<t-area-card
					:title="store.getDistrictName"
					:is-loading="isLoading"
					:min-width="400"
					:max-width="400"
				>
					<template #chart>
						<t-donut-chart
							:labels="
								store.getDistrictStat.map(item => item.name)
							"
							:series="
								store.getDistrictStat.map(item => item.count)
							"
							:height="350"
							:enable-logarithmic="false"
							:log-base="10"
							:y-start-value="0"
							legend-position="bottom"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isPreviousLoading"
							@click="previousInterval"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next>
						<v-btn
							color="primary"
							:loading="isNextLoading"
							@click="nextInterval"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #interval v-if="!isLoading">
						{{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }} -
						{{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
					</template>
				</t-area-card>
			</v-container>
		</v-col>
		<v-col cols="auto" v-for="region of store.getRegions" :key="region">
			<v-container>
				<t-area-card
					:title="region.name"
					:is-loading="isLoading"
					:min-width="400"
					:max-width="400"
				>
					<template #chart>
						<t-donut-chart
							:labels="region?.stat?.map(item => item.name)"
							:series="region?.stat?.map(item => item.count)"
							:height="350"
							:enable-logarithmic="false"
							:log-base="10"
							:y-start-value="0"
							legend-position="bottom"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isPreviousLoading"
							@click="previousInterval"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next>
						<v-btn
							color="primary"
							:loading="isNextLoading"
							@click="nextInterval"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #interval v-if="!isLoading">
						{{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }} -
						{{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
					</template>
				</t-area-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import {
		TAreaCard,
		TDonutChart,
		TFilterSidebar,
	} from '../components/widgets'
	import { useDistrictStore } from '../stores/district'
	import { dateFormat, getLastMonth } from '@/utils/utils'
	import { ref, computed, onMounted } from 'vue'
	import { useRoute } from 'vue-router'
	import { toast } from 'vue-sonner'

	const route = useRoute()
	const store = useDistrictStore()

	const leftMenu = ref(false)
	const rail = ref(false)
	const isPreviousLoading = ref(false)
	const isNextLoading = ref(false)
	const loadingSubjects = ref(false)
	const errorSubjects = ref(null)
	const loadingStatistics = ref(false)
	const errorStatistics = ref(null)

	// Вычисляемое свойство для общего состояния загрузки
	const isLoading = computed(() => {
		return store.isLoading || loadingStatistics.value
	})

	// Формирование параметров запроса
	const getParams = () => {
		const params = {
			startDate: store.startDate,
			endDate: store.endDate,
		}
		if (store.selectedRegions.length > 0) {
			params.regions = store.selectedRegions.toString()
		}
		return params
	}

	// Переход к предыдущему интервалу
	const previousInterval = async () => {
		try {
			isPreviousLoading.value = true
			loadingStatistics.value = true
			errorStatistics.value = null

			// Сдвигаем дату на месяц назад относительно текущего startDate
			const currentStart = new Date(store.startDate)
			console.log(currentStart)

			const newInterval = getLastMonth(currentStart)
			store.startDate = newInterval.startDate
			store.endDate = newInterval.endDate

			const parameters = getParams()
			await store.loadStatisticsAPI(route.params.label, parameters)
		} catch (e) {
			errorStatistics.value = e.message
			store.dropStatistics()
		} finally {
			isPreviousLoading.value = false
			loadingStatistics.value = false
		}
	}

	// Переход к следующему интервалу
	const nextInterval = async () => {
		try {
			// Сдвигаем дату на месяц вперёд относительно текущего endDate
			const currentStart = new Date(store.startDate)
			currentStart.setMonth(currentStart.getMonth() + 1)

			if (currentStart > new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}

			currentStart.setMonth(currentStart.getMonth() + 1)

			isNextLoading.value = true
			loadingStatistics.value = true
			errorStatistics.value = null

			const newInterval = getLastMonth(currentStart)
			store.startDate = newInterval.startDate
			store.endDate = newInterval.endDate

			const parameters = getParams()
			await store.loadStatisticsAPI(route.params.label, parameters)
		} catch (e) {
			errorStatistics.value = e.message
			store.dropStatistics()
		} finally {
			isNextLoading.value = false
			loadingStatistics.value = false
		}
	}

	// Загрузка начальных данных
	const loadInitialData = async () => {
		try {
			loadingSubjects.value = true
			errorSubjects.value = null
			await store.loadSubjectsAPI(route.params.label)

			loadingStatistics.value = true
			errorStatistics.value = null
			store.initializeForm() // Инициализируем форму из стора
			const parameters = getParams()
			await store.loadStatisticsAPI(route.params.label, parameters)
		} catch (e) {
			errorSubjects.value = e.message
			errorStatistics.value = e.message
			store.dropStatistics()
		} finally {
			loadingSubjects.value = false
			loadingStatistics.value = false
		}
	}

	onMounted(async () => {
		await loadInitialData()
	})
</script>

<style scoped></style>
