<template>
	<v-app>
		<v-app-bar color="primary">
			<v-toolbar-title>Капибара</v-toolbar-title>
			<template v-slot:prepend>
				<v-app-bar-nav-icon />
			</template>
			<template v-slot:append>
				<v-btn
					v-if="currentRouteName == 'home'"
					@click="goToDashboard()"
					prepend-icon="mdi-monitor-dashboard"
					variant="plain"
				>
					Статистика
				</v-btn>

				<v-btn
					v-if="currentRouteName == 'dashboard'"
					@click="goToHome()"
					prepend-icon="mdi-home"
					variant="plain"
				>
					На главную
				</v-btn>
			</template>
		</v-app-bar>

		<router-view></router-view>
	</v-app>
</template>

<script lang="js">
	export default {
		name: 'app',
		components: {},
		computed: {
			currentRouteName() {
				console.log(this.$route.name == 'home')

				return this.$route.name
			},
		},
		methods: {
			async goToDashboard() {
				await this.$router.push({
					name: 'dashboard',
				})
				console.log('go to Dashboard')
			},
			async goToHome() {
				await this.$router.push({
					name: 'home',
				})
				console.log('go to Home')
			},
		},
	}
</script>

<style scoped></style>
