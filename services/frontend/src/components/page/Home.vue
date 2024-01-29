<template>
	<v-app>
		<v-row>
			<v-col>
				<v-container>
					<v-app-bar color="primary">
						<v-toolbar-title><strong>Home</strong></v-toolbar-title>
						<template v-slot:prepend>
							<v-app-bar-nav-icon
								icon="mdi-home"
								:ripple="false"
							/>
						</template>
						<template v-slot:append>
							<v-btn
								@click="goToLogin()"
								prepend-icon="mdi-login"
								variant="plain"
								:ripple="false"
							>
								<strong>Login</strong>
							</v-btn>
							<!-- <v-btn
								@click="goToSignUp()"
								prepend-icon="mdi-monitor-dashboard"
								variant="plain"
								:ripple="false"
							>
								<strong>Sign Up</strong>
							</v-btn> -->
							<v-btn
								@click="goToDashboard()"
								prepend-icon="mdi-monitor-dashboard"
								variant="plain"
								:ripple="false"
							>
								<strong>Dashboard</strong>
							</v-btn>
						</template>
					</v-app-bar>
				</v-container>
			</v-col>
		</v-row>
		<v-row>
			<v-col>
				<wellcome-card />
			</v-col>
		</v-row>
	</v-app>
</template>

<script lang="js">
	import { VAppBarNavIcon } from 'vuetify/lib/components/index.mjs'
	import { WellcomeCard } from '../widget'

	export default {
		name: 'home',
		components: { VAppBarNavIcon, WellcomeCard },
		data() {
			return {}
		},

		methods: {
			async goToDashboard() {
				await this.$router.push({
					name: 'dashboard',
				})
				console.log('go to Dashboard')
			},
			async goToLogin() {
				await this.$router.push({
					name: 'login',
				})
				console.log('go to Login')
			},
			async goToSignUp() {
				await this.$router.push({
					name: 'sign-up',
				})
				console.log('go to Sign Up')
			},
		},
	}
</script>

<style scoped></style>
