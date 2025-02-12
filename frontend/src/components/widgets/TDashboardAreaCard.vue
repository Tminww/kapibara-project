<template>
	<v-card
		:loading="isLoading"
		:max-width="maxWidth"
		:max-height="maxHeight"
		:width
		:height
		elevation="10"
	>
		<v-card-title class="title-wrap">
			{{ title }}
		</v-card-title>

		<v-card-subtitle v-if="subtitle">
			{{ subtitle }}
		</v-card-subtitle>

		<v-card-text class="pb-0">
			<slot name="chart" />
		</v-card-text>
		<v-card-actions class="justify-space-between">
			<slot name="previous"></slot>
			<div class="time-wrap">
				<slot name="quarter"></slot>
			</div>
			<slot name="next"></slot>
		</v-card-actions>
		<slot name="error"></slot>
	</v-card>
</template>

<script setup>
	const props = defineProps({
		title: { type: String, required: false, default: 'Область' },
		subtitle: {
			type: String,
			required: false,
			default: 'Происходит что-то',
		},
		width: { type: Number, required: false },
		maxHeight: { type: Number, required: false },
		height: { type: Number, required: false },
		maxWidth: { type: Number, required: false },
		isLoading: { type: Boolean, required: true, default: true },
	})
</script>

<style scoped>
	.title-wrap {
		white-space: normal; /* Позволяет перенос строк */
		word-wrap: break-word; /* Переносит слова, если они длинные */
		overflow-wrap: break-word;
		max-width: 100%; /* Ограничивает ширину заголовка */
		text-align: left; /* По желанию, можно выровнять текст */
	}

	.time-wrap {
		flex: 1; /* Занимает всю доступную ширину */
		text-align: center; /* Центрирует текст */
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
