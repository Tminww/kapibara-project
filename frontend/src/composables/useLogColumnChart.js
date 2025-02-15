import { ref, onMounted, computed } from 'vue'

import { useSubjectStore } from '@/stores'
import { getLastYear } from '@/utils/utils'

import { toast } from 'vue-sonner'

export function useLogColumnChart() {
	const subjectStore = useSubjectStore()
	const AreaError = ref(null)
	const AreaDate = ref(new Date())
	const isAreaPreviousLoading = ref(false)
	const isAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isAreaLoading = computed(() => {
		return subjectStore.isLoading || isStatisticsLoading.value
	})
	const AreaYear = computed(() => {
		console.log(AreaDate.value)

		const { startDate, endDate } = getLastYear(AreaDate.value)
		console.log('AreaYear', startDate, endDate)
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
		Array.isArray(subjectStore.statistics.stat)
			? subjectStore.statistics.stat
			: [],
	)

	const AreaSeries = computed(() => data.value.map(row => row.count))

	const AreaLabels = computed(() => data.value.map(row => row.name))

	const AreaPreviousYear = async () => {
		try {
			AreaError.value = null
			isAreaPreviousLoading.value = true
			AreaDate.value = new Date(
				AreaDate.value.setFullYear(AreaDate.value.getFullYear() - 1),
			)

			const parameters = getLastYear(AreaDate.value)

			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			AreaError.value = e.message
		} finally {
			isAreaPreviousLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			AreaError.value = null
			isStatisticsLoading.value = true
			const parameters = getLastYear()

			await subjectStore.loadAreaDocumentsStatisticsByYear(parameters)
		} catch (e) {
			AreaError.value = e.message
			subjectStore.dropStatistics()
		} finally {
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})

	return {
		AreaLabels,
		AreaSeries,
		AreaError,
		AreaDate,
		AreaYear,
		isAreaPreviousLoading,
		isAreaNextLoading,
		isAreaLoading,
		AreaPreviousYear,
	}
}
