import { ref, onMounted, computed } from 'vue'

import { useDashboardStore } from '../stores/dashboard'
import { getLastMonth } from '@/utils/utils'

import { toast } from 'vue-sonner'

export function useSecondDashboardArea() {
	const statisticStore = useDashboardStore()
	const secondAreaError = ref(null)
	const secondAreaDate = ref(new Date())
	const isSecondAreaPreviousLoading = ref(false)
	const isSecondAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isSecondAreaLoading = computed(() => {
		return (
			isSecondAreaPreviousLoading.value ||
			isSecondAreaNextLoading.value ||
			isStatisticsLoading.value
		)
	})
	const secondAreaMonth = computed(() => {
		const { startDate, endDate } = getLastMonth(secondAreaDate.value)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')

		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const data = computed(() =>
		Array.isArray(statisticStore.getSecondAreaDocumentsStatisticsByMonth)
			? statisticStore.getSecondAreaDocumentsStatisticsByMonth
			: [],
	)

	const secondAreaSeries = computed(() => data.value.map(row => row.count))

	const secondAreaLabels = computed(() => data.value.map(row => row.name))

	const secondAreaPreviousMonth = async () => {
		try {
			secondAreaError.value = null
			isSecondAreaPreviousLoading.value = true
			secondAreaDate.value = new Date(
				secondAreaDate.value.setMonth(
					secondAreaDate.value.getMonth() - 1,
				),
			)

			const parameters = getLastMonth(secondAreaDate.value)

			await statisticStore.loadSecondAreaDocumentsStatisticsByMonth(
				parameters,
			)
		} catch (e) {
			secondAreaError.value = e.message
		} finally {
			isSecondAreaPreviousLoading.value = false
		}
	}

	const secondAreaNextMonth = async () => {
		try {
			secondAreaError.value = null
			isSecondAreaNextLoading.value = true
			if (secondAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			secondAreaDate.value = new Date(
				secondAreaDate.value.setMonth(
					secondAreaDate.value.getMonth() + 1,
				),
			)

			const parameters = getLastMonth(secondAreaDate.value)

			await statisticStore.loadSecondAreaDocumentsStatisticsByMonth(
				parameters,
			)
		} catch (e) {
			secondAreaError.value = e.message
		} finally {
			isSecondAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			secondAreaError.value = null
			isStatisticsLoading.value = true
			const parameters = getLastMonth()

			await statisticStore.loadSecondAreaDocumentsStatisticsByMonth(
				parameters,
			)
		} catch (e) {
			secondAreaError.value = e.message
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
	}
}
