<template>
	<div
		class="skeleton ellipse"
		:class="{ animation: animation }"
		:style="{
			width: size.width + 'px',
			height: size.height + 'px',
			left: position.left + 'px',
			top: position.top + 'px',
			backgroundColor: fill,
			opacity: fillOpacity,
			border: strokeWidth + 'px solid ' + stroke,
			borderRadius: '50%',
		}"
	></div>
</template>

<script setup>
	const props = defineProps({
		size: {
			type: Object,
			required: true,
			default: () => ({ width: 50, height: 50 }),
		},
		position: {
			type: Object,
			required: true,
			default: () => ({ left: 0, top: 0 }),
		},
		fill: {
			type: String,
			default: '#d1d1d1',
		},
		fillOpacity: {
			type: Number,
			default: 1,
		},
		stroke: {
			type: String,
			default: '#000000',
		},
		strokeOpacity: {
			type: Number,
			default: 0,
		},
		strokeWidth: {
			type: Number,
			default: 0,
		},
		animation: {
			type: Boolean,
			default: true, // По умолчанию включена анимация
		},
	})
</script>

<style scoped>
	.ellipse {
		position: absolute;
	}
	.animation {
		animation: shimmer-diagonal 2s infinite linear;

		background: linear-gradient(
			to bottom right,
			#e0e0e0 20%,
			#ffffff 50%,
			#e0e0e0 70%
		);
		background-repeat: no-repeat;
		background-size: 300% 300%; /* Увеличиваем размер фона для диагональной анимации */
	}

	@keyframes shimmer-diagonal {
		0% {
			background-position: 100% 100%; /* Начальная позиция: левый верхний угол */
		}

		100% {
			background-position: 0 0; /* Конечная позиция: правый нижний угол */
		}
	}
</style>
