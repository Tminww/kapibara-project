<template>
	<div class="date-picker">
		<div class="selected-date" @click="showPicker = !showPicker">
			{{ formattedDate }}
		</div>

		<div v-if="showPicker" class="picker">
			<div class="year-selector">
				<button @click="changeYear(-1)">←</button>
				<span>{{ pickerYear }}</span>
				<button @click="changeYear(1)">→</button>
			</div>

			<div class="month-grid">
				<button
					v-for="(month, index) in months"
					:key="index"
					@click="selectMonth(index)"
				>
					{{ month }}
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { computed, ref, watch } from 'vue'

	const props = defineProps({
		modelValue: {
			type: Date,
			required: true,
		},
	})

	const emit = defineEmits(['update:modelValue'])

	const selectedDate = computed({
		get: () => props.modelValue,
		set: value => emit('update:modelValue', value),
	})

	const showPicker = ref(false)
	const pickerYear = ref(selectedDate.value.getFullYear())

	const months = [
		'январь',
		'февраль',
		'март',
		'апрель',
		'май',
		'июнь',
		'июль',
		'август',
		'сентябрь',
		'октябрь',
		'ноябрь',
		'декабрь',
	]

	const formattedDate = computed(() => {
		const month = months[selectedDate.value.getMonth()]
		const year = selectedDate.value.getFullYear()
		return `${month} ${year} г.`
	})

	watch(showPicker, isOpen => {
		if (isOpen) {
			pickerYear.value = selectedDate.value.getFullYear()
		}
	})

	function selectMonth(monthIndex) {
		const newDate = new Date(pickerYear.value, monthIndex, 1)
		selectedDate.value = newDate
		showPicker.value = false
	}

	function changeYear(delta) {
		pickerYear.value += delta
	}
</script>

<style scoped>
	.date-picker {
		position: relative;
		display: inline-block;
		font-family: Arial, sans-serif;
	}

	.selected-date {
		padding: 8px 12px;
		border: 1px solid #ccc;
		border-radius: 4px;
		cursor: pointer;
		background-color: white;
	}

	.picker {
		position: absolute;
		top: 100%;
		left: 0;
		margin-top: 4px;
		padding: 12px;
		border: 1px solid #ccc;
		border-radius: 4px;
		background-color: white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		z-index: 1000;
	}

	.year-selector {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 8px;
	}

	.year-selector button {
		padding: 4px 8px;
		border: 1px solid #ccc;
		border-radius: 4px;
		background-color: white;
		cursor: pointer;
	}

	.month-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 4px;
	}

	.month-grid button {
		padding: 8px;
		border: 1px solid #ccc;
		border-radius: 4px;
		background-color: white;
		cursor: pointer;
		white-space: nowrap;
	}

	.month-grid button:hover {
		background-color: #f0f0f0;
	}
</style>
