<template>
	<h1>Hello App!</h1>
	<p>
		<!-- <router-link to="/">Go to Home</router-link> -->
		<router-link to="/dashboard">Go to Dashboard</router-link>
	</p>
	<router-view></router-view>
</template>

<script lang="js">
	export default {
		name: 'app',
		components: {},
	}
</script>

<style scoped></style>
