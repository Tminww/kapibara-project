<template>
	<v-form class="form-container" @submit.prevent="onFormSubmit()">
		<div v-for="district in districts" :key="district.id">
			<v-select
				cache-items
				density="comfortable"
				clearable
				multiple
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
						class="text-grey text-caption align-self-center"
					>
						(+{{ selectedSubjects[district.id].length - 1 }} другие)
					</span>
				</template>
			</v-select>
		</div>

		<v-divider class="mb-5"></v-divider>

		<v-select
			density="comfortable"
			variant="outlined"
			@update:modelValue="e => comboBoxModelUpdate(e)"
			label="Выбор периода"
			:items="[
				'За прошлый месяц',
				'За прошлый квартал',
				'За прошлый год',
			]"
		>
		</v-select>

		<div class="group-date">
			<v-text-field
				class="items"
				@update:modelValue="e => startDateModelUpdate(e)"
				placeholder="yyyy-mm-dd"
				density="default"
				variant="solo"
				type="date"
				:value="startDate"
			>
				<!-- {{ startDate }} -->
			</v-text-field>

			<v-text-field
				class="items"
				@update:modelValue="e => endDateModelUpdate(e)"
				placeholder="yyyy-mm-dd"
				density="default"
				variant="solo"
				type="date"
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
				color="green"
				text="Применить"
			/>

			<v-btn class="items" text="Отменить" color="red" />
		</div>
	</v-form>
	<!-- <date-picker v-model="selectedDate" />
	<p>Selected Date: {{ selectedDate }}</p> -->

	<!-- <div v-if="errorStatistics">{{ errorStatistics }}</div> -->
</template>

<script lang="js">
	// import RequestSelect from './RequestSelect.vue'
	import DatePicker from './DatePicker.vue'
	import { mapGetters, mapActions } from 'vuex'
	import {
		getLastYear,
		getLastMonth,
		getLastQuarter,
	} from '../../utils/utils.js'

	export default {
		name: 'request-form',
		components: { DatePicker },
		props: {
			districts: { type: Object, required: true },
		},
		emits: ['loadingSuccessful', 'loadingError'],

		data() {
			return {
				loadingStatistics: false,
				errorStatistics: null,
				startDate: null,
				endDate: null,
				selectedSubjects: {},
				selectedDate: '',
			}
		},
		computed: {
			...mapGetters(['getStatistics']),
			// getSubjectItemsAndId() {
			//     const regionInfo = {}
			//     for (const region of this.district.regions) {
			//         regionInfo({ name: region.name, id: region.id })
			//     }
			//     return regionInfo
			// },
		},

		methods: {
			...mapActions(['updateStatisticsAPI', 'dropStatistics']),
			getSubjectItemsAndId(district) {
				let regionInfo = []
				for (const region of district.regions) {
					regionInfo.push({ name: region.name, id: region.id })
				}
				return regionInfo
			},

			paramsProcessing(selected, startDate, endDate) {
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
			},

			setDefaultValue() {
				this.loadingStatistics = false
				this.errorStatistics = null
				this.startDate = null
				this.endDate = null
				this.selectedSubjects = {}
			},
			async onFormSubmit(event) {
				try {
					this.loadingStatistics = true
					this.errorStatistics = null

					const parameters = this.paramsProcessing(
						this.selectedSubjects,
						this.startDate,
						this.endDate,
					)
					await this.updateStatisticsAPI(parameters)
					this.$emit('loadingSuccessful')
				} catch (e) {
					this.errorStatistics = e.message
					this.dropStatistics()
					this.$emit('loadingError')
				} finally {
					this.loadingStatistics = false
					// this.setDefaultValue()
				}
			},

			selectModelUpdate(id, data) {
				// Reflect.set(this.selectedSubjects, 'id', data)
				this.selectedSubjects[id] = data
			},
			startDateModelUpdate(data) {
				if (data.trim() === '') {
					this.startDate = null
				} else {
					this.startDate = data
				}
			},
			endDateModelUpdate(data) {
				if (data.trim() === '') {
					this.endDate = null
				} else {
					this.endDate = data
				}
			},
			comboBoxModelUpdate(data) {
				if (data === 'За прошлый месяц') {
					const interval = getLastMonth()
					this.startDate = interval.startDate
					this.endDate = interval.endDate
				} else if (data === 'За прошлый квартал') {
					const interval = getLastQuarter()
					this.startDate = interval.startDate
					this.endDate = interval.endDate
				} else if (data === 'За прошлый год') {
					const interval = getLastYear()
					this.startDate = interval.startDate
					this.endDate = interval.endDate
				}
				// console.table(this.startDate, this.endDate)
			},
		},
		mounted() {},
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
