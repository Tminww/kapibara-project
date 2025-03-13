<template>
	<v-navigation-drawer
		location="left"
		temporary
		:width="500"
		elevation="3"
		v-model="internalLeftMenu"
		permanent
		:rail="rail"
		@click="updateRail(false)"
	>
		<v-list-item nav>
			<v-list-item-title>
				<h2 class="font-weight-bold pl-2">Настроить фильтры</h2>
			</v-list-item-title>
			<template #append>
				<v-btn
					icon="mdi-chevron-left"
					variant="text"
					@click.stop="toggleMenu"
				></v-btn>
			</template>
		</v-list-item>
		<v-divider></v-divider>
		<v-container>
			<v-alert
				v-if="errorSubjects"
				class="d-flex align-center justify-center"
				type="error"
				title="Произошла ошибка"
				:text="errorSubjects"
				variant="tonal"
			></v-alert>
			<v-progress-circular
				v-else-if="loadingSubjects"
				class="d-flex align-center justify-center"
				indeterminate
			/>
			<t-filter-form v-else :regions="regions" />
		</v-container>
	</v-navigation-drawer>
</template>

<script setup>
	import { computed } from 'vue'
	import { TFilterForm } from './'

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
		rail: {
			type: Boolean,
			default: false,
		},
		loadingSubjects: {
			type: Boolean,
			default: false,
		},
		errorSubjects: {
			type: String,
			default: '',
		},
		regions: {
			type: Array,
			default: () => [],
		},
	})

	const emits = defineEmits(['update:modelValue', 'update:rail'])

	const internalLeftMenu = computed({
		get: () => props.modelValue,
		set: value => emits('update:modelValue', value),
	})

	const toggleMenu = () => {
		internalLeftMenu.value = !internalLeftMenu.value
	}

	const updateRail = value => {
		emits('update:rail', value)
	}
</script>

<style scoped>
	.card-container {
		display: flex;
		flex-direction: column;
		max-height: 90vh;
		overflow: hidden;
		width: 100%; /* Гарантируем, что контейнер занимает всю ширину */
		padding: 0; /* Убираем внутренние отступы */
		margin: 0; /* Убираем внешние отступы */
		box-sizing: border-box; /* Учитываем padding и border в ширине */
	}

	.full-width-card {
		width: 100% !important; /* Переопределяем ширину */
		max-width: none !important; /* Убираем ограничения max-width */
		min-width: 0 !important; /* Убираем минимальную ширину */
		box-sizing: border-box; /* Учитываем padding и border в ширине */
		padding: 0 !important; /* Убираем внутренние отступы карточки */
		margin: 0 !important; /* Убираем внешние отступы карточки */
		/* Отладка: временно добавьте для проверки границ */
		/* outline: 1px solid red; */
	}

	.title-wrap {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.subtitle-wrap {
		white-space: normal;
		word-wrap: break-word;
		overflow-wrap: break-word;
		max-width: 100%;
		text-align: left;
		font-size: 14px;
		height: 20px;
	}

	.time-wrap {
		flex: 1;
		text-align: center;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.chart-wrap {
		width: 100%;
		height: 350px;
		min-height: 200px;
	}

	.scrollable {
		flex: 1;
		max-height: 60vh;
		overflow-y: auto;
		overflow-x: hidden;
		scroll-behavior: smooth;
	}

	/* Адаптивность для маленьких экранов */
	@media (max-height: 896px) {
		.scrollable {
			max-height: 50vh;
		}
		.chart-wrap {
			height: 300px;
		}
	}

	@media (max-height: 667px) {
		.scrollable {
			max-height: 40vh;
		}
		.chart-wrap {
			height: 250px;
		}
	}
</style>
