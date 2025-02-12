<template>
	<div>
		<input v-model="selectedDate" type="text" @click="showDatePicker" />
		<div v-if="show" class="date-picker">
			<div class="header">
				<button @click="previousMonth">&lt;</button>
				<div>{{ currentMonth }}</div>
				<button @click="nextMonth">&gt;</button>
			</div>
			<div class="weekdays">
				<div v-for="day in weekdays" :key="day">{{ day }}</div>
			</div>
			<div class="days">
				<div
					v-for="day in allDays"
					:key="day"
					:class="{ selected: day === selectedDate }"
					@click="selectDate(day)"
				>
					{{ day }}
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, computed } from 'vue'

	const selectedDate = ref('')
	const show = ref(false)
	const currentDate = ref(new Date())

	const currentMonth = computed(() => {
		return currentDate.value.toLocaleString('default', { month: 'long' })
	})

	const weekdays = computed(() => [
		'Sun',
		'Mon',
		'Tue',
		'Wed',
		'Thu',
		'Fri',
		'Sat',
	])

	const allDays = computed(() => {
		const year = currentDate.value.getFullYear()
		const month = currentDate.value.getMonth()
		const firstDay = new Date(year, month, 1)
		const lastDay = new Date(year, month + 1, 0)
		const days = []

		for (let i = 1; i <= lastDay.getDate(); i++) {
			days.push(i)
		}

		return days
	})

	const showDatePicker = () => {
		show.value = true
	}

	const previousMonth = () => {
		currentDate.value = new Date(
			currentDate.value.setMonth(currentDate.value.getMonth() - 1),
		)
	}

	const nextMonth = () => {
		currentDate.value = new Date(
			currentDate.value.setMonth(currentDate.value.getMonth() + 1),
		)
	}

	const selectDate = day => {
		selectedDate.value = day
		show.value = false
	}
</script>

<style scoped>
	.date-picker {
		background-color: #fff;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
		position: absolute;
		top: 30px;
		left: 0;
		right: 0;
		z-index: 999;
		display: flex;
		flex-direction: column;
	}

	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px;
	}

	.weekdays {
		display: flex;
		justify-content: space-between;
		padding: 10px;
		border-bottom: 1px solid #ccc;
	}

	.days {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 5px;
		padding: 10px;
		max-width: 280px;
	}

	.selected {
		background-color: #ccc;
		border-radius: 4px;
		cursor: pointer;
	}

	button {
		cursor: pointer;
		border: none;
		background-color: transparent;
	}
</style>
