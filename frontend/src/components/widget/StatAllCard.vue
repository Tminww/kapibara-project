<template>
	<v-card class="mx-auto" elevation="8" max-width="500" hover>
		<v-toolbar dense flat class="text-h6 mb-1 px-4" color="red lighten-2">
			{{ all.name }}
		</v-toolbar>
		<v-card-title class="text-h6 mb-1">
			Всего НПА: {{ all.count }}
		</v-card-title>

		<v-card-text>
			<div class="justify-center">
				<doughnut-chart v-if="loaded" :chartData :chartOptions />
			</div>
		</v-card-text>
	</v-card>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue'
	import DoughnutChart from './DoughnutChart.vue'

	const props = defineProps({
		all: { type: Object, required: true },
	})

	const loaded = ref(false)

	const chartData = computed(() => {
		let data = []
		console.info(props.all.stat)

		for (const row of props.all.stat) {
			console.log(row.count)
			data.push(row.count)
		}

		return {
			name: 'series-1',
			data,
		}
	})

	const chartOptions = computed(() => {
		let categories = []

		for (const row of props.all.stat) {
			categories.push(row.name)
		}
		return [
			{
				chart: {
					id: 'vuechart-stat-all-card',
				},
				xaxis: {
					categories,
				},
			},
		]
	})

	onMounted(() => {
		console.log('ALL', props.all)
		loaded.value = true
	})
</script>

<style scoped></style>
