import { ref, onMounted, computed } from 'vue'

import { useStatisticStore } from '@/stores'
import { getLastYear } from '@/utils/utils'

import { toast } from 'vue-sonner'

export function useFirstDashboardArea() {
	const statisticStore = useStatisticStore()
	const firstAreaError = ref(null)
	const firstAreaDate = ref(new Date())
	const isFirstAreaPreviousLoading = ref(false)
	const isFirstAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isFirstAreaLoading = computed(() => {
		return statisticStore.isLoading || isStatisticsLoading.value
	})
	const firstAreaYear = computed(() => {
		console.log(firstAreaDate.value)

		const { startDate, endDate } = getLastYear(firstAreaDate.value)
		console.log('FirstAreaYear', startDate, endDate)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')
		console.table({
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		})
		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const data = computed(() =>
		Array.isArray(statisticStore.statistics.stat)
			? statisticStore.statistics.stat
			: [],
	)

	const firstAreaSeries = computed(() => data.value.map(row => row.count))

	const firstAreaLabels = computed(() => data.value.map(row => row.name))

	const firstAreaPreviousYear = async () => {
		try {
			firstAreaError.value = null
			isFirstAreaPreviousLoading.value = true
			firstAreaDate.value = new Date(
				firstAreaDate.value.setFullYear(
					firstAreaDate.value.getFullYear() - 1,
				),
			)

			const parameters = getLastYear(firstAreaDate.value)

			await statisticStore.loadFirstAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			firstAreaError.value = e.message
		} finally {
			isFirstAreaPreviousLoading.value = false
		}
	}

	const firstAreaNextYear = async () => {
		try {
			firstAreaError.value = null
			isFirstAreaNextLoading.value = true
			if (firstAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			firstAreaDate.value = new Date(
				firstAreaDate.value.setFullYear(
					firstAreaDate.value.getFullYear() + 1,
				),
			)

			const parameters = getLastYear(firstAreaDate.value)

			await statisticStore.loadFirstAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			firstAreaError.value = e.message
		} finally {
			isFirstAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			firstAreaError.value = null
			isStatisticsLoading.value = true
			const parameters = getLastYear()

			await statisticStore.loadFirstAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			firstAreaError.value = e.message
			statisticStore.dropStatistics()
		} finally {
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})

	return {
		firstAreaLabels,
		firstAreaSeries,
		firstAreaError,
		firstAreaDate,
		firstAreaYear,
		isFirstAreaPreviousLoading,
		isFirstAreaNextLoading,
		isFirstAreaLoading,
		firstAreaPreviousYear,
		firstAreaNextYear,
	}
}
