<template>
	<v-form class="form-container" @submit.prevent="onFormSubmit">
		<v-checkbox
			v-for="region in regions"
			:key="region.id"
			color="primary"
			:label="region.name"
			:value="region.id"
			v-model="form.selectedSubjects"
			label="region.name"
			value="region.id"
			hide-details
			density="compact"
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
			@update:modelValue="comboBoxModelUpdate"
		></v-select>

		<div class="group-date">
			<v-text-field
				class="items"
				v-model="form.startDate"
				placeholder="yyyy-mm-dd"
				density="compact"
				variant="outlined"
				type="date"
			/>
			<v-text-field
				class="items"
				v-model="form.endDate"
				placeholder="yyyy-mm-dd"
				density="compact"
				variant="outlined"
				type="date"
			/>
		</div>

		<div class="group-botton">
			<v-btn
				class="items"
				type="submit"
				:loading="loadingStatistics"
				color="primary"
				variant="tonal"
				text="Применить"
			/>
			<v-btn
				class="items"
				text="Отменить"
				color="red"
				variant="tonal"
				@click="setDefaultValue"
			/>
		</div>
	</v-form>
</template>

<script setup>
	import { onMounted, reactive, ref } from 'vue'
	import { getLastYear, getLastMonth, getLastQuarter } from '@/utils/utils.js'
	import { useDistrictStore } from '../../stores/district'

	const store = useDistrictStore()

	// Пропсы
	const props = defineProps({
		regions: { type: Array, required: true },
	})

	// Реактивный объект для хранения значений формы
	const form = reactive({
		startDate: null,
		endDate: null,
		selectedSubjects: store.getSubjects.map(s => s.id),
		selectedPeriod: 'За прошлый месяц',
	})

	const loadingStatistics = ref(false)
	const errorStatistics = ref(null)

	// Формирование параметров запроса
	const paramsProcessing = (selected, startDate, endDate) => {
		const params = {}
		if (startDate) params.startDate = startDate
		if (endDate) params.endDate = endDate

		// Объединяем все выбранные регионы в один массив

		if (selected.length > 0) {
			params.regions = selected.toString()
		}
		return params
	}

	// Сброс значений формы
	const setDefaultValue = () => {
		loadingStatistics.value = false
		errorStatistics.value = null
		form.startDate = null
		form.endDate = null
		form.selectedSubjects = store.getSubjects.map(s => s.id)
		form.selectedPeriod = 'За прошлый месяц'
		comboBoxModelUpdate('За прошлый месяц')
	}

	// Обработчик отправки формы
	const onFormSubmit = async () => {
		try {
			console.log('onFormSubmit', form)
			await store.startLoading()
			loadingStatistics.value = true
			errorStatistics.value = null

			const parameters = paramsProcessing(
				form.selectedSubjects,
				form.startDate,
				form.endDate,
			)
			console.log('parameters', parameters)
			await store.loadStatisticsAPI(store.getDistrictName, parameters)
		} catch (e) {
			errorStatistics.value = e.message
			store.dropStatistics()
		} finally {
			loadingStatistics.value = false
			await store.endLoading()
		}
	}

	// Обновление дат в зависимости от выбора периода
	const comboBoxModelUpdate = selection => {
		let interval
		switch (selection) {
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
		form.startDate = interval.startDate
		form.endDate = interval.endDate
	}
	onMounted(() => {
		comboBoxModelUpdate('За прошлый месяц')
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
		min-width: 150px; /* Минимальная ширина для адаптивности */
	}
</style>
