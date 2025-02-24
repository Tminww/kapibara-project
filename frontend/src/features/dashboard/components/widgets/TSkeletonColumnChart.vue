<template>
	<div class="skeleton-container">
		<div class="skeleton-wrapper">
			<Rectangle
				v-for="(pos, index) in rectPositions"
				:key="index"
				:size="{ width: pos.width, height: pos.height }"
				:position="{ left: pos.left, top: pos.top }"
			/>
		</div>
	</div>
</template>

<script setup>
	import { TSkeletonRectangle as Rectangle } from '../ui/'

	const rectPositions = [
		{ left: 50, bot: 0, width: 30, height: 10 },
		{ left: 100, bot: 0, width: 30, height: 70 },
		{ left: 150, bot: 0, width: 30, height: 150 },
		{ left: 200, bot: 0, width: 30, height: 200 },
		{ left: 250, bot: 0, width: 30, height: 150 },
		{ left: 300, bot: 0, width: 30, height: 200 },
		{ left: 350, bot: 0, width: 30, height: 40 },
		{ left: 400, bot: 0, width: 30, height: 20 },
		{ left: 450, bot: 0, width: 30, height: 60 },
		{ left: 500, bot: 0, width: 30, height: 130 },
		{ left: 550, bot: 0, width: 30, height: 180 },
		{ left: 600, bot: 0, width: 30, height: 200 },
		{ left: 650, bot: 0, width: 30, height: 130 },
		{ left: 700, bot: 0, width: 30, height: 200 },
		{ left: 750, bot: 0, width: 30, height: 170 },
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
		flex-direction: row;
		align-items: flex-end;
		justify-content: center;
		width: auto;
		height: auto;
		min-width: 200px;
		min-height: 250px;
	}
</style>
