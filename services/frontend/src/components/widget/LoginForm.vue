<template>
	<v-app>
		<div class="d-flex align-center justify-center" style="height: 100vh">
			<v-main class="d-flex justify-center align-center">
				<v-col cols="10" lg="4" class="mx-auto">
					<v-card
						class="mx-auto pa-12 pb-8"
						elevation="8"
						max-width="448"
						rounded="lg"
					>
						<h2>Vuetify Login Form</h2>
						<div class="text-subtitle-1 text-medium-emphasis">
							Account
						</div>
						<v-text-field
							density="compact"
							placeholder="Email address"
							prepend-inner-icon="mdi-email-outline"
							variant="outlined"
							clearable
						></v-text-field>
						<div
							class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
						>
							Password
							<a
								class="text-caption text-decoration-none text-blue"
								href="#"
								rel="noopener noreferrer"
								target="_blank"
							>
								Forgot login password?</a
							>
						</div>
						<v-text-field
							:append-inner-icon="
								visible ? 'mdi-eye-off' : 'mdi-eye'
							"
							:type="visible ? 'text' : 'password'"
							density="compact"
							placeholder="Enter your password"
							prepend-inner-icon="mdi-lock-outline"
							variant="outlined"
							@click:append-inner="visible = !visible"
							clearable
						></v-text-field>

						<v-card
							class="mb-12"
							color="surface-variant"
							variant="tonal"
						>
							<v-card-text
								class="text-medium-emphasis text-caption"
							>
								Warning: After 3 consecutive failed login
								attempts, you account will be temporarily locked
								for three hours. If you must login now, you can
								also click "Forgot login password?" below to
								reset the login password.
							</v-card-text>
						</v-card>

						<v-btn
							block
							class="mb-8"
							color="blue"
							size="large"
							variant="tonal"
						>
							Log In
						</v-btn>

						<v-card-text class="text-center">
							<router-link :to="{ name: 'sign-up' }">
								Sign up now
								<v-icon icon="mdi-chevron-right"></v-icon
							></router-link>
						</v-card-text>
					</v-card>
				</v-col>
			</v-main>
		</div>
	</v-app>
	<router-view></router-view>
</template>
<script>
	export default {
		data() {
			return {
				visible: false,
				loading: false,
				snackbar: false,
				passwordShow: false,
				email: '',
				emailRules: [
					v => !!v || 'E-mail is required',
					v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
				],
				password: '',
				passwordRules: [
					v => !!v || 'Password is required',
					v =>
						(v && v.length >= 6) ||
						'Password must be 6  characters or more!',
				],
			}
		},
		methods: {
			submitHandler() {
				if (this.$refs.form.validate()) {
					this.loading = true
					setTimeout(() => {
						this.loading = false
						this.snackbar = true
					}, 3000)
				}
			},
		},
	}
</script>

<style scoped></style>
