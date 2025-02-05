<template>
	<v-card class="mx-auto" elevation="8" max-width="500" hover>
		<v-toolbar
			dense
			flat
			class="text-h6 mb-1 px-4"
			color="primary lighten-2"
			>{{ district.name }}
		</v-toolbar>
		<v-card-title class="text-h6 mb-1">
			Всего НПА: {{ district.count }}
		</v-card-title>

		<v-card-text>
			<div class="justify-center">
				<doughnut-chart
					v-if="loaded"
					:chart-data="chartData"
					:chart-options="chartOptions"
				/>
			</div>
		</v-card-text>

		<v-card-actions class="justify-center">
			<v-btn color="primary" @click="dialog = true"> Детально </v-btn>

			<v-dialog
				v-model="dialog"
				fullscreen
				transition="dialog-bottom-transition"
			>
				<v-card>
					<v-toolbar dark color="primary">
						<v-toolbar-title
							>Статистика за {{ district.name }}</v-toolbar-title
						>
						<v-spacer></v-spacer>
						<v-toolbar-items>
							<v-btn icon dark @click="dialog = false">
								<v-icon>mdi-close</v-icon>
							</v-btn>
						</v-toolbar-items>
					</v-toolbar>
					<v-card-text>
						<v-row justify="center">
							<v-col v-for="region in district.regions">
								<stat-region-card :region="region" />
							</v-col>
						</v-row>
					</v-card-text>
					<v-card-actions>
						<v-btn color="primary" block @click="dialog = false"
							>Закрыть статистику
						</v-btn>
					</v-card-actions>
				</v-card>
			</v-dialog>
		</v-card-actions>
	</v-card>
</template>
<script setup>
	import { ref, computed, onMounted } from 'vue'
	import DoughnutChart from './DoughnutChart.vue'
	import StatRegionCard from './StatRegionCard.vue'

	const props = defineProps({
		district: { type: Object, required: true },
	})

	const loaded = ref(false)
	const dialog = ref(false)

	const chartOptions = computed(() => {
		let categories = []
		for (const row of props.district.stat) {
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
	const chartData = computed(() => {
		let data = []

		for (const row of props.district.stat) {
			data.push(row.count)
		}

		return {
			name: 'series-1',
			data,
		}
	})

	onMounted(() => {
		console.log('DISTRICT', props.district)
		loaded.value = true
	})
</script>
<style scoped></style>
