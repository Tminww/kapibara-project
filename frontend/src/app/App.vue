<template>
	<v-app>
		<dashboard-layout>
			<router-view> </router-view>
		</dashboard-layout>
	</v-app>
</template>

<script setup>
	import { DashboardLayout } from '@/layouts'
</script>

<style scoped></style>
