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
			<v-progress-circular
				v-if="loading"
				class="d-flex align-center justify-center"
				indeterminate
			/>
			<slot v-else name="form"></slot>
		</v-container>
	</v-navigation-drawer>
</template>

<script setup>
	import { computed } from 'vue'

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
		loading: {
			type: Boolean,
			default: false,
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
