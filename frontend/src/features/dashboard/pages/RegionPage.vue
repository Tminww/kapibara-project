<template>
	<!-- Фильтры в боковом меню -->
	<t-filter-sidebar v-model="leftMenu" :loading="loadingSubjects">
		<template #form>
			<t-filter-form
				:loading="store.isLoading"
				:items="store.getSubjects"
				@submit="data => onSubmit(data)"
			></t-filter-form>
		</template>
	</t-filter-sidebar>

	<v-row no-gutters class="justify-start">
		<v-col>
			<v-container fluid class="my-0 py-0">
				<v-btn
					color="primary"
					variant="tonal"
					@click="leftMenu = !leftMenu"
				>
					Фильтры
				</v-btn>
			</v-container>
		</v-col>
	</v-row>
	<v-row v-if="errorStatistics || errorSubjects">
		<v-col>
			<v-container fluid>
				<v-alert
					v-if="errorSubjects"
					class="d-flex align-center justify-center"
					type="error"
					title="Произошла ошибка"
					:text="errorStatistics || errorSubjects"
					variant="tonal"
				></v-alert>
			</v-container>
		</v-col>
	</v-row>
	<v-row v-else no-gutters class="justify-space-around">
		<v-col cols="auto">
			<v-container>
				<t-region-card
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
				</t-region-card>
			</v-container>
		</v-col>
		<v-col cols="auto" v-for="region of store.getRegions" :key="region">
			<v-container>
				<t-region-card
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
				</t-region-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import {
		TRegionCard,
		TDonutChart,
		TFilterSidebar,
		TFilterForm,
	} from '../components/widgets'
	import { useDistrictStore } from '../stores/district'
	import { dateFormat, getLastMonth } from '@/utils/utils'
	import { ref, computed, onMounted } from 'vue'
	import { useRoute } from 'vue-router'
	import { toast } from 'vue-sonner'

	const route = useRoute()
	const store = useDistrictStore()

	const leftMenu = ref(false)
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
	const convertDateToYYYYMMDDString = date => {
		const year = date.getFullYear()
		const month = String(date.getMonth() + 1).padStart(2, '0') // +1, так как месяцы с 0
		const day = String(date.getDate()).padStart(2, '0')
		const yyyyMMdd = `${year}-${month}-${day}`
		return yyyyMMdd
	}

	const onSubmit = async data => {
		// Обработчик отправки формы (синхронизация с Pinia Store)
		console.log('start')
		try {
			await store.startLoading()

			// Синхронизируем локальные данные с Pinia Store
			store.selectedItems = [...form.selectedItems]
			store.selectedPeriod = form.selectedPeriod
			store.startDate = convertDateToYYYYMMDDString(form.startDate) // Передаём строку
			store.endDate = convertDateToYYYYMMDDString(form.endDate) // Передаём строку

			const parameters = paramsProcessing(
				store.selectedItems,
				store.startDate,
				store.endDate,
			)
			await store.loadStatisticsAPI(store.getDistrictName, parameters)
		} catch (e) {
			store.dropStatistics()
		} finally {
			await store.endLoading()
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
