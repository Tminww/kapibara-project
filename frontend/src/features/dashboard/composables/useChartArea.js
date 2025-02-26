import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

export function useChartArea({
	loadData,
	dropData,
	getInterval,
	interval = 'quarter',
}) {
	const error = ref(null)
	const date = ref(new Date())
	const isPreviousLoading = ref(false)
	const isNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isDataLoading = computed(() => {
		return (
			isPreviousLoading.value ||
			isNextLoading.value ||
			isStatisticsLoading.value
		)
	})
	const currentInterval = computed(() => {
		const { startDate, endDate } = getInterval(date.value)
		const [startYear, startMonth, startDay] = startDate.split('-')
		const [endYear, endMonth, endDay] = endDate.split('-')

		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})

	const previousInterval = async () => {
		try {
			error.value = null
			isPreviousLoading.value = true

			if (interval === 'week') {
				date.value = new Date(
					date.value.setDate(date.value.getDate() - 7),
				)
			} else if (interval === 'quarter') {
				date.value.setDate(1)
				date.value = new Date(
					date.value.setMonth(date.value.getMonth() - 3),
				)
			} else if (interval === 'month') {
				date.value.setDate(1)

				date.value = new Date(
					date.value.setMonth(date.value.getMonth() - 1),
				)
			} else if (interval === 'year') {
				date.value.setDate(1)

				date.value = new Date(
					date.value.setFullYear(date.value.getFullYear() - 1),
				)
			} else {
				return Error('В указанном интервале ошибка')
			}

			const parameters = getInterval(date.value)

			await loadData(parameters)
		} catch (e) {
			error.value = e.message
		} finally {
			isPreviousLoading.value = false
		}
	}

	const nextInterval = async () => {
		try {
			error.value = null
			isNextLoading.value = true

			if (date.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}

			if (interval === 'week') {
				date.value = new Date(
					date.value.setDate(date.value.getDate() + 7),
				)
			} else if (interval === 'quarter') {
				date.value.setDate(1)
				date.value = new Date(
					date.value.setMonth(date.value.getMonth() + 3),
				)
			} else if (interval === 'month') {
				date.value.setDate(1)

				date.value = new Date(
					date.value.setMonth(date.value.getMonth() + 1),
				)
			} else if (interval === 'year') {
				date.value.setDate(1)

				date.value = new Date(
					date.value.setFullYear(date.value.getFullYear() + 1),
				)
			} else {
				return Error('В указанном интервале ошибка')
			}

			const parameters = getInterval(date.value)

			await loadData(parameters)
		} catch (e) {
			error.value = e.message
		} finally {
			isNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			error.value = null
			isStatisticsLoading.value = true

			const parameters = getInterval()

			await loadData(parameters)
		} catch (e) {
			error.value = e.message
			dropData()
		} finally {
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})

	return {
		error,
		currentInterval,
		isPreviousLoading,
		isNextLoading,
		isDataLoading,
		previousInterval,
		nextInterval,
	}
}
