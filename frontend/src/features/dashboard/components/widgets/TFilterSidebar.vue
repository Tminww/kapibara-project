<template>
	<v-navigation-drawer
		location="left"
		temporary
		:width="500"
		elevation="10"
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
