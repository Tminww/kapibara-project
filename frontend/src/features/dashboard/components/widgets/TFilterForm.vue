<template>
	<v-form class="form-container" @submit.prevent="onFormSubmit">
		<v-checkbox
			v-for="region in props.regions"
			:key="region.id"
			color="primary"
			:label="region.name"
			:value="region.id"
			v-model="form.selectedRegions"
			hide-details
			density="compact"
			@update:modelValue="ensureAtLeastOneSelected"
		></v-checkbox>
		<v-divider class="my-4"></v-divider>

		<v-select
			density="comfortable"
			variant="outlined"
			label="Выбрать период"
			v-model="form.selectedPeriod"
			:items="[
				'За прошлый месяц',
				'За прошлый квартал',
				'За прошлый год',
			]"
			@update:modelValue="updateDatesByPeriod"
		></v-select>

		<div class="group-date">
			<v-date-input
				label="Дата начала"
				placeholder="DD.MM.YYYY"
				prepend-icon=""
				prepend-inner-icon="$calendar"
				variant="outlined"
				v-model="form.startDate"
				@update:model-value="val => console.log(val)"
			></v-date-input>
			<v-date-input
				label="Дата окончания"
				placeholder="DD.MM.YYYY"
				prepend-icon=""
				prepend-inner-icon="$calendar"
				variant="outlined"
				v-model="form.endDate"
			></v-date-input>
		</div>

		<div class="group-botton">
			<v-btn
				class="items"
				type="submit"
				:loading="store.isLoading"
				color="primary"
				variant="tonal"
				text="Применить"
			/>
			<v-btn
				class="items"
				text="Отменить"
				color="red"
				variant="tonal"
				@click="resetForm"
			/>
		</div>
	</v-form>
</template>

<script setup>
	import { onMounted, reactive } from 'vue'
	import { useDistrictStore } from '../../stores/district'
	import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils.js'
	import { VDateInput } from 'vuetify/labs/VDateInput'

	const store = useDistrictStore()

	const props = defineProps({
		regions: { type: Array, required: true },
	})

	// Локальное реактивное состояние формы
	const form = reactive({
		selectedRegions: [],
		selectedPeriod: 'За прошлый месяц',
		startDate: null, // Ожидаем строку в формате yyyy-mm-dd или null
		endDate: null, // Ожидаем строку в формате yyyy-mm-dd или null
	})

	// Убеждаемся, что хотя бы один регион остаётся выбранным
	const ensureAtLeastOneSelected = newValue => {
		if (newValue.length === 0) {
			// Если массив пустой, возвращаем последний выбранный регион
			form.selectedRegions = [
				form.selectedRegions[0] || props.regions[0].id,
			]
		}
	}
	// Обновление дат по выбранному периоду (локально)
	const updateDatesByPeriod = period => {
		let interval
		switch (period) {
			case 'За прошлый месяц':
				interval = getLastMonth()
				break
			case 'За прошлый квартал':
				interval = getLastQuarter()
				break
			case 'За прошлый год':
				interval = getLastYear()
				break
			default:
				interval = { startDate: null, endDate: null }
		}
		// Убеждаемся, что даты всегда в формате строки yyyy-mm-dd
		form.startDate = new Date(interval.startDate)
		form.endDate = new Date(interval.endDate)
	}

	// Сброс формы (локально, с использованием начальных значений из стора)
	const resetForm = () => {
		form.selectedRegions = props.regions.map(s => s.id) // Все регионы из пропсов
		form.selectedPeriod = 'За прошлый месяц'
		updateDatesByPeriod(form.selectedPeriod)
	}

	const convertDateToYYYYMMDDString = date => {
		const year = date.getFullYear()
		const month = String(date.getMonth() + 1).padStart(2, '0') // +1, так как месяцы с 0
		const day = String(date.getDate()).padStart(2, '0')
		const yyyyMMdd = `${year}-${month}-${day}`
		return yyyyMMdd
	}

	// Формирование параметров запроса
	const paramsProcessing = (selected, startDate, endDate) => {
		const params = {}
		console.log('startDate', convertDateToYYYYMMDDString(startDate))
		if (startDate) params.startDate = convertDateToYYYYMMDDString(startDate)
		if (endDate) params.endDate = convertDateToYYYYMMDDString(endDate)
		if (selected.length > 0) params.regions = selected.toString()
		return params
	}

	// Обработчик отправки формы (синхронизация с Pinia Store)
	const onFormSubmit = async () => {
		try {
			await store.startLoading()

			// Синхронизируем локальные данные с Pinia Store
			store.selectedRegions = [...form.selectedRegions]
			store.selectedPeriod = form.selectedPeriod
			store.startDate = form.startDate // Передаём строку
			store.endDate = form.endDate // Передаём строку

			const parameters = paramsProcessing(
				store.selectedRegions,
				store.startDate,
				store.endDate,
			)
			await store.loadStatisticsAPI(store.getDistrictName, parameters)
		} catch (e) {
			console.error('Ошибка:', e.message)
			store.dropStatistics()
		} finally {
			await store.endLoading()
		}
	}

	onMounted(() => {
		store.subjects = props.regions // Устанавливаем регионы в стор
		// Инициализируем локальную форму начальными значениями
		form.selectedRegions = props.regions.map(s => s.id)
		form.selectedPeriod = 'За прошлый месяц'
		updateDatesByPeriod(form.selectedPeriod)
	})
</script>

<style scoped>
	.form-container {
		display: flex;
		flex-direction: column;
	}
	.group-botton,
	.group-date {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
		width: 100%;
		gap: 10px;
	}
	.items {
		flex: 1;
		min-width: 150px;
	}
</style>
