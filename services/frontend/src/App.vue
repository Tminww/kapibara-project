<template>
	<v-app>
		<v-app-bar color="primary" prominent>
			<template v-slot:prepend>
				<v-app-bar-nav-icon />
			</template>
			<template v-slot:append>
				<v-btn
					@click="goToDashboard()"
					icon="mdi-monitor-dashboard"
				></v-btn>
			</template>
			<v-toolbar-title>Капибара</v-toolbar-title>
		</v-app-bar>
	</v-app>
</template>

<script lang="js">
	export default {
		name: 'app',
		components: {},
		methods: {
			async goToDashboard() {
				await this.$router.push({
					name: 'dashboard',
				})
				console.log('go to Dashboard')
			},
		},
	}
</script>

<style scoped></style>
