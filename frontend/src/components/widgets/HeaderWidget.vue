<template>
	<v-app-bar :color="color" scroll-behavior="elevate" scroll-threshold="100">
		<template #title>
			<div class="cursor-pointer">
				<slot name="title"></slot>
			</div>
		</template>

		<template #append>
			<div class="cursor-pointer pr-10">
				<slot name="login"></slot>
			</div>
		</template>
	</v-app-bar>
</template>

<script setup>
	import { defineProps } from 'vue'
	defineProps({
		color: {
			type: String,
			default: 'primary',
		},
	})
</script>
