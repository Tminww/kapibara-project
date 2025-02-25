import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

import { useDashboardStore } from '../store'
import { getLastQuarter } from '@/utils/utils.js'

export function useSixthDashboardArea() {
	const statisticStore = useDashboardStore()
	const sixthAreaError = ref(null)
	const sixthAreaDate = ref(new Date())
	const isSixthAreaPreviousLoading = ref(false)
	const isSixthAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isSixthAreaLoading = computed(() => {
		return (
			isSixthAreaPreviousLoading.value ||
			isSixthAreaNextLoading.value ||
			isStatisticsLoading.value
		)
	})
	const sixthAreaQuarter = computed(() => {
		const { startDate, endDate } = getLastQuarter(sixthAreaDate.value)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')
		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const data = computed(() =>
		Array.isArray(statisticStore.getSixthAreaDocumentsStatisticsByQuarter)
			? statisticStore.getSixthAreaDocumentsStatisticsByQuarter
			: [],
	)

	const sixthAreaSeries = computed(() => data.value.map(row => row.count))

	const sixthAreaLabels = computed(() => data.value.map(row => row.name))
	const sixthAreaPreviousQuarter = async () => {
		try {
			sixthAreaError.value = null
			isSixthAreaPreviousLoading.value = true
			sixthAreaDate.value = new Date(
				sixthAreaDate.value.setMonth(
					sixthAreaDate.value.getMonth() - 3,
				),
			)

			const parameters = getLastQuarter(sixthAreaDate.value)

			await statisticStore.loadSixthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			sixthAreaError.value = e.message
		} finally {
			isSixthAreaPreviousLoading.value = false
		}
	}

	const sixthAreaNextQuarter = async () => {
		try {
			sixthAreaError.value = null
			isSixthAreaNextLoading.value = true
			if (sixthAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			sixthAreaDate.value = new Date(
				sixthAreaDate.value.setMonth(
					sixthAreaDate.value.getMonth() + 3,
				),
			)

			const parameters = getLastQuarter(sixthAreaDate.value)

			await statisticStore.loadSixthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			sixthAreaError.value = e.message
		} finally {
			isSixthAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			sixthAreaError.value = null
			isStatisticsLoading.value = true

			const parameters = getLastQuarter()

			await statisticStore.loadSixthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			sixthAreaError.value = e.message
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
	}
}
