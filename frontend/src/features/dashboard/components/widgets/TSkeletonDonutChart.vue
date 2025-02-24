<template>
	<div class="skeleton-container">
		<div class="skeleton-wrapper">
			<Ellipse
				:size="{ width: 235, height: 235 }"
				:position="{ left: 0, top: 0 }"
			/>
			<Ellipse
				:size="{ width: 141, height: 141 }"
				:position="{ left: 47, top: 47 }"
				fill="#ffffff"
				:animation="false"
			/>
			<Ellipse
				v-for="(pos, index) in ellipsePositions"
				:key="index"
				:size="{ width: 15, height: 15 }"
				:position="{ left: pos.left, top: pos.top }"
			/>
			<Rectangle
				v-for="(pos, index) in rectPositions"
				:key="index"
				:size="{ width: 74, height: 7 }"
				:position="{ left: pos.left, top: pos.top }"
			/>
		</div>
	</div>
</template>

<script setup>
	import {
		TSkeletonRectangle as Rectangle,
		TSkeletonEllipse as Ellipse,
	} from '../ui/'

	const ellipsePositions = [
		{ left: 250, top: 35 },
		{ left: 250, top: 55 },
		{ left: 250, top: 75 },
		{ left: 250, top: 95 },
		{ left: 250, top: 115 },
		{ left: 250, top: 135 },
		{ left: 250, top: 155 },
		{ left: 250, top: 175 },
	]

	const rectPositions = [
		{ left: 275, top: 39 },
		{ left: 275, top: 59 },
		{ left: 275, top: 79 },
		{ left: 275, top: 99 },
		{ left: 275, top: 119 },
		{ left: 275, top: 139 },
		{ left: 275, top: 159 },
		{ left: 275, top: 179 },
	]
</script>

<style scoped>
	.skeleton-container {
		position: relative;
		width: 100%;
		height: 100%;
		background: white;
		padding-left: 20px;
		padding-top: 20px;
	}

	.skeleton-wrapper {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: auto;
		height: auto;
		min-width: 200px;
		min-height: 250px;
	}
</style>
