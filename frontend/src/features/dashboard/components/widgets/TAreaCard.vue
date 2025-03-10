<template>
	<v-card
		:loading="isLoading"
		:max-width="maxWidth"
		:min-width="minWidth"
		:max-height="maxHeight"
		:width="width"
		:height="height"
		elevation="3"
	>
		<v-card-title class="title-wrap mt-2">
			{{ title }}
		</v-card-title>

		<v-card-subtitle class="subtitle-wrap" v-if="subtitle">
			{{ subtitle }}
		</v-card-subtitle>

		<v-card-text class="scrollable pb-0 pt-0">
			<div v-if="isLoading" class="loader-wrap">
				<t-icon name="dashboard-gray" :width="200" :height="200" />
			</div>
			<div v-else class="chart-wrap">
				<slot name="chart" />
			</div>
		</v-card-text>

		<v-card-actions class="justify-space-between">
			<slot name="previous"></slot>
			<div class="text-h7 time-wrap">
				<slot name="interval"></slot>
			</div>
			<slot name="next"></slot>
		</v-card-actions>
	</v-card>
</template>

<script setup>
	import { TIcon } from '@/components/ui'
	const props = defineProps({
		title: { type: String, required: false, default: 'Область' },
		subtitle: {
			type: String,
			required: false,
		},
		width: { type: Number, required: false },
		maxHeight: { type: Number, required: false },
		height: { type: Number, required: false },
		maxWidth: { type: Number, required: false },
		minWidth: { type: Number, required: false },
		isLoading: { type: Boolean, required: true, default: true },
	})
</script>

<style scoped>
	.title-wrap {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.subtitle-wrap {
		white-space: normal; /* Позволяет перенос строк */
		word-wrap: break-word; /* Переносит слова, если они длинные */
		overflow-wrap: break-word;
		max-width: 100%; /* Ограничивает ширину заголовка */
		text-align: left; /* По желанию, можно выровнять текст */
		font-size: 14px;
		height: 20px;
		/* font-weight: bold; */
	}

	.time-wrap {
		flex: 1; /* Занимает всю доступную ширину */
		text-align: center; /* Центрирует текст */
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.chart-wrap {
		height: 350px;
	}

	.scrollable {
		overflow-x: none; /* Горизонтальная прокрутка при необходимости */
	}
	.loader-wrap {
		display: flex;
		justify-content: center;
		align-items: center;
		width: auto;
		height: 350px;
	}
</style>
