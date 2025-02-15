<template>
	<v-form class="form-container" @submit.prevent="onFormSubmit">
		<div v-for="district in districts" :key="district.id">
			<v-select
				class="mb-3"
				color="primary"
				density="comfortable"
				clearable
				multiple
				rounded
				hide-details
				variant="outlined"
				:label="district.name"
				item-title="name"
				item-value="id"
				:items="getSubjectItemsAndId(district)"
				:model-value="form.selectedSubjects[district.id] || []"
				@update:modelValue="
					value => (form.selectedSubjects[district.id] = value)
				"
			>
				<template v-slot:selection="{ item, index }">
					<div v-if="index < 1">
						<span>{{ item.title }}</span>
					</div>
					<span
						v-if="index === 1"
						class="text-caption align-self-center"
					>
						(+{{
							(form.selectedSubjects[district.id] || []).length -
							1
						}}
						другие)
					</span>
				</template>
			</v-select>
		</div>

		<v-divider class="my-4"></v-divider>

		<v-select
			density="comfortable"
			variant="outlined"
			rounded
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
				rounded
			/>
			<v-text-field
				class="items"
				v-model="form.endDate"
				placeholder="yyyy-mm-dd"
				density="compact"
				variant="outlined"
				type="date"
				rounded
			/>
		</div>

		<div class="group-botton">
			<v-btn
				class="items"
				type="submit"
				:loading="loadingStatistics"
				color="primary"
				variant="tonal"
				rounded
				text="Применить"
			/>
			<v-btn
				class="items"
				text="Отменить"
				color="red"
				rounded
				variant="tonal"
				@click="setDefaultValue"
			/>
		</div>
	</v-form>
</template>

<script setup>
	import { reactive, ref } from 'vue'
	import { getLastYear, getLastMonth, getLastQuarter } from '@/utils/utils.js'
	import { useSubjectStore } from '@/stores/'

	const subjectStore = useSubjectStore()

	// Пропсы
	const props = defineProps({
		districts: { type: Object, required: true },
	})

	// Реактивный объект для хранения значений формы
	const form = reactive({
		startDate: null,
		endDate: null,
		selectedSubjects: {},
		selectedPeriod: null,
	})

	const loadingStatistics = ref(false)
	const errorStatistics = ref(null)

	// Возвращает список регионов для селекта
	const getSubjectItemsAndId = district => {
		return district.regions.map(region => ({
			name: region.name,
			id: region.id,
		}))
	}

	// Формирование параметров запроса
	const paramsProcessing = (selected, startDate, endDate) => {
		const params = {}
		if (startDate) params.startDate = startDate
		if (endDate) params.endDate = endDate

		// Объединяем все выбранные регионы в один массив
		const subjects = Object.values(selected).flat()
		if (subjects.length > 0) {
			params.regions = subjects.toString()
		}
		return params
	}

	// Сброс значений формы
	const setDefaultValue = () => {
		loadingStatistics.value = false
		errorStatistics.value = null
		form.startDate = null
		form.endDate = null
		form.selectedSubjects = {}
		form.selectedPeriod = null
	}

	// Обработчик отправки формы
	const onFormSubmit = async () => {
		try {
			console.log('onFormSubmit', form)
			await subjectStore.startLoading()
			loadingStatistics.value = true
			errorStatistics.value = null

			const parameters = paramsProcessing(
				form.selectedSubjects,
				form.startDate,
				form.endDate,
			)
			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			errorStatistics.value = e.message
			subjectStore.dropStatistics()
		} finally {
			loadingStatistics.value = false
			await subjectStore.endLoading()
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
