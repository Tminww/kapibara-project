<template>
	<v-navigation-drawer
		location="left"
		temporary
		floating
		:width="350"
		v-model="internalLeftMenu"
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
		<v-container class="scrollable-container">
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

	const emits = defineEmits(['update:modelValue'])

	const internalLeftMenu = computed({
		get: () => props.modelValue,
		set: value => emits('update:modelValue', value),
	})

	const toggleMenu = () => {
		internalLeftMenu.value = !internalLeftMenu.value
	}
</script>

<style scoped>
	/* Стили для контейнера с прокруткой */
	.scrollable-container {
		max-height: calc(
			100vh - 120px
		); /* Учитываем высоту заголовка и отступы */
		overflow-y: auto; /* Включаем вертикальную прокрутку */
		overflow-x: hidden; /* Отключаем горизонтальную прокрутку */
		scroll-behavior: smooth; /* Плавная прокрутка */
	}

	/* Опционально: настройка полосы прокрутки */
	.scrollable-container::-webkit-scrollbar {
		width: 5px; /* Ширина полосы прокрутки */
	}

	.scrollable-container::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.3); /* Цвет бегунка */
		border-radius: 4px; /* Закругление бегунка */
		padding-right: 5px;
	}

	.scrollable-container::-webkit-scrollbar-track {
		background: transparent; /* Фон полосы прокрутки */
	}

	/* Адаптивность для меньших экранов */
	@media (max-height: 667px) {
		.scrollable-container {
			max-height: calc(
				100vh - 100px
			); /* Уменьшаем высоту на малых экранах */
		}
	}
</style>
