<template>
	<v-form class="form-container" @submit.prevent="onFormSubmit()">
		<div v-for="district in districts" :key="district.id">
			<v-select
				class="mb-3"
				color="primary"
				cache-items
				density="comfortable"
				clearable
				multiple
				rounded
				hide-details
				variant="outlined"
				@update:modelValue="e => selectModelUpdate(district.id, e)"
				:label="district.name"
				item-title="name"
				item-value="id"
				:items="getSubjectItemsAndId(district)"
			>
				<template v-slot:selection="{ item, index }">
					<div v-if="index < 1">
						<span>{{ item.title }}</span>
					</div>
					<span
						v-if="index === 1"
						class="text-caption align-self-center"
					>
						(+{{ selectedSubjects[district.id].length - 1 }} другие)
					</span>
				</template>
			</v-select>
		</div>

		<h3 class="font-weight-bold pl-2 mt-5">Выбрать временной промежуток</h3>
		<v-divider class="mb-5"></v-divider>

		<v-select
			density="comfortable"
			variant="outlined"
			rounded
			@update:modelValue="e => comboBoxModelUpdate(e)"
			label="Выбрать период"
			:items="[
				'За прошлый месяц',
				'За прошлый квартал',
				'За прошлый год',
			]"
		>
		</v-select>
		<!-- <v-date-input
			class="mb-2"
			v-model="rangeDates"
			variant="outlined"
			prepend-icon=""
			prepend-inner-icon=""
			label="Выбрать временной интервал"
			max-width="360"
			multiple="range"
			hide-details
			rounded
			density="compact"
			placeholder="DD.MM.YYYY - DD.MM.YYYY"
			@update:model-value="onSubmit"
		></v-date-input> -->
		<div class="group-date">
			<v-text-field
				class="items"
				@update:modelValue="e => startDateModelUpdate(e)"
				placeholder="yyyy-mm-dd"
				density="compact"
				variant="outlined"
				type="date"
				rounded
				:value="startDate"
			>
				<!-- {{ startDate }} -->
			</v-text-field>

			<v-text-field
				class="items"
				@update:modelValue="e => endDateModelUpdate(e)"
				placeholder="yyyy-mm-dd"
				density="compact"
				variant="outlined"
				type="date"
				rounded
				:value="endDate"
			>
				<!-- {{ endDate }} -->
			</v-text-field>
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

			<!-- <v-btn
				class="items"
				text="Отменить"
				color="red"
				rounded
				variant="tonal"
			/> -->
		</div>
	</v-form>
</template>
<script setup>
	import { ref, computed } from 'vue'
	import { VDateInput } from 'vuetify/labs/VDateInput'
	import { getLastYear, getLastMonth, getLastQuarter } from '@/utils/utils.js'
	import { useStatisticStore } from '@/stores/statisticStore' // Импортируем store
	import { useDate } from 'vuetify'

	const date = useDate()

	const rangeDates = async () => {
		console('rangeDates', date.getWeekArray(new Date()))
	}
	// Инициализация store
	const statisticStore = useStatisticStore()

	// Пропсы
	const props = defineProps({
		districts: { type: Object, required: true },
	})

	// Эмиты

	// Реактивные переменные
	const loadingStatistics = ref(false)
	const errorStatistics = ref(null)
	const startDate = ref(null)
	const endDate = ref(null)
	const selectedSubjects = ref({})
	const selectedDate = ref('')

	// Метод для получения списка регионов и их ID
	const getSubjectItemsAndId = district => {
		return district.regions.map(region => ({
			name: region.name,
			id: region.id,
		}))
	}

	// Метод для обработки параметров запроса
	const paramsProcessing = (selected, startDate, endDate) => {
		const params = {}
		if (startDate !== null) {
			params['startDate'] = startDate
		}
		if (endDate !== null) {
			params['endDate'] = endDate
		}

		const subjects = []
		for (const subjectsInDistrict of Object.values(selected)) {
			for (const subjectId of subjectsInDistrict) {
				subjects.push(subjectId)
			}
		}
		if (subjects.length > 0) {
			params['regions'] = subjects.toString()
		}
		return params
	}

	// Метод для сброса значений формы
	const setDefaultValue = () => {
		loadingStatistics.value = false
		errorStatistics.value = null
		startDate.value = null
		endDate.value = null
		selectedSubjects.value = {}
	}

	// Метод для отправки формы
	const onFormSubmit = async event => {
		try {
			await statisticStore.startLoading()
			loadingStatistics.value = true
			errorStatistics.value = null

			const parameters = paramsProcessing(
				selectedSubjects.value,
				startDate.value,
				endDate.value,
			)
			await statisticStore.updateStatisticsAPI(parameters)
		} catch (e) {
			errorStatistics.value = e.message
			statisticStore.dropStatistics()
		} finally {
			loadingStatistics.value = false
			await statisticStore.endLoading()
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения
		}
	}

	// Метод для обновления выбранных регионов
	const selectModelUpdate = (id, data) => {
		selectedSubjects.value[id] = data
	}

	// Метод для обновления начальной даты
	const startDateModelUpdate = data => {
		startDate.value = data.trim() === '' ? null : data
	}

	// Метод для обновления конечной даты
	const endDateModelUpdate = data => {
		endDate.value = data.trim() === '' ? null : data
	}

	// Метод для обновления даты в зависимости от выбора в комбобоксе
	const comboBoxModelUpdate = data => {
		let interval
		switch (data) {
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
		startDate.value = interval.startDate
		endDate.value = interval.endDate
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
		flex-wrap: wrap;
	}

	.items {
		flex-grow: 1;
		margin: 0 10px;
	}
</style>
