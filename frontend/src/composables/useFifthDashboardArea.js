import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

import { useStatisticStore } from '@/stores/'
import { getLastQuarter } from '@/utils/utils.js'

export function useFifthDashboardArea() {
	const statisticStore = useStatisticStore()
	const fifthAreaError = ref(null)
	const fifthAreaDate = ref(new Date())
	const isFifthAreaPreviousLoading = ref(false)
	const isFifthAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isFifthAreaLoading = computed(() => {
		return (
			isFifthAreaPreviousLoading.value ||
			isFifthAreaNextLoading.value ||
			isStatisticsLoading.value
		)
	})
	const fifthAreaQuarter = computed(() => {
		const { startDate, endDate } = getLastQuarter(fifthAreaDate.value)
		console.log('FifthAreaQuarter', startDate, endDate)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')
		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const data = computed(() =>
		Array.isArray(statisticStore.getFifthAreaDocumentsStatisticsByQuarter)
			? statisticStore.getFifthAreaDocumentsStatisticsByQuarter
			: [],
	)

	const fifthAreaSeries = computed(() => data.value.map(row => row.count))

	const fifthAreaLabels = computed(() => data.value.map(row => row.name))
	const fifthAreaPreviousQuarter = async () => {
		try {
			fifthAreaError.value = null
			isFifthAreaPreviousLoading.value = true
			fifthAreaDate.value = new Date(
				fifthAreaDate.value.setMonth(
					fifthAreaDate.value.getMonth() - 3,
				),
			)

			const parameters = getLastQuarter(fifthAreaDate.value)

			await statisticStore.loadFifthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			fifthAreaError.value = e.message
		} finally {
			isFifthAreaPreviousLoading.value = false
		}
	}

	const fifthAreaNextQuarter = async () => {
		try {
			fifthAreaError.value = null
			isFifthAreaNextLoading.value = true
			if (fifthAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			fifthAreaDate.value = new Date(
				fifthAreaDate.value.setMonth(
					fifthAreaDate.value.getMonth() + 3,
				),
			)

			const parameters = getLastQuarter(fifthAreaDate.value)

			await statisticStore.loadFifthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			fifthAreaError.value = e.message
		} finally {
			isFifthAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			fifthAreaError.value = null
			isStatisticsLoading.value = true

			const parameters = getLastQuarter()

			await statisticStore.loadFifthAreaDocumentsStatisticsByQuarter(
				parameters,
			)
		} catch (e) {
			fifthAreaError.value = e.message
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
	}
}
