<template>
	<v-card
		:loading="isLoading"
		:max-width="maxWidth"
		:min-width="minWidth"
		:max-height="maxHeight"
		:width
		:height
		elevation="3"
	>
		<v-card-title class="title-wrap mt-2">
			{{ title }}
		</v-card-title>

		<v-card-subtitle class="subtitle-wrap" v-if="subtitle">
			{{ subtitle }}
		</v-card-subtitle>

		<v-card-text class="pb-0 pt-0">
			<slot name="filter"></slot>
			<slot name="chart" />
		</v-card-text>

		<div class="time-wrap">
			<slot name="interval"></slot>
		</div>
		<slot name="error"></slot>
	</v-card>
</template>

<script setup>
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
		white-space: normal; /* Позволяет перенос строк */
		word-wrap: break-word; /* Переносит слова, если они длинные */
		overflow-wrap: break-word;
		max-width: 100%; /* Ограничивает ширину заголовка */
		text-align: left; /* По желанию, можно выровнять текст */
		font-size: 20px;
		font-weight: bold;
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
		font-size: 20px;
		margin-top: 10px;
		margin-bottom: 10px;
	}
</style>
