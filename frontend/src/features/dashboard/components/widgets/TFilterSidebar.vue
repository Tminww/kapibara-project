<template>
	<!-- Добавляем v-overlay вручную -->
	<div class="sidebar-wrapper">
		<v-navigation-drawer
			location="left"
			temporary
			floating
			:width="350"
			v-model="internalLeftMenu"
			:scrim="true"
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
			<v-container class="scrollable-container pt-0">
				<v-progress-circular
					v-if="loading"
					class="d-flex align-center justify-center"
					indeterminate
				/>
				<slot v-else name="form"></slot>
			</v-container>
		</v-navigation-drawer>
	</div>
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
		max-height: calc(100vh - 120px);
		overflow-y: auto;
		overflow-x: hidden;
		scroll-behavior: smooth;
	}

	.scrollable-container::-webkit-scrollbar {
		width: 5px;
	}

	.scrollable-container::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
		padding-right: 5px;
	}

	.scrollable-container::-webkit-scrollbar-track {
		background: transparent;
	}

	@media (max-height: 667px) {
		.scrollable-container {
			max-height: calc(100vh - 100px);
		}
	}

	/* Стили для затемнения */
	:deep(.v-navigation-drawer__scrim) {
		position: fixed !important;
		top: 0 !important;
		left: 0 !important;
		width: 100vw !important;
		height: 100vh !important;
		z-index: 1000 !important; /* Убедимся, что затемнение выше контента */
		background-color: rgba(0, 0, 0, 0.5) !important; /* Цвет затемнения */
	}
</style>
