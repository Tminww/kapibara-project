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
						<v-form v-model="form" @submit.prevent="onSubmit">
							<h2 class="d-flex justify-center align-center">
								Аутентификация
							</h2>
							<div class="text-subtitle-1 text-medium-emphasis">
								Логин
							</div>
							<v-text-field
								autofocus
								density="compact"
								placeholder="Введите имя пользователя"
								prepend-inner-icon="mdi-account-outline"
								variant="outlined"
								clearable
								v-model="username"
								:readonly="loading"
								:rules="[required, usernameRules]"
							></v-text-field>
							<div
								class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
							>
								Пароль
							</div>
							<v-text-field
								:append-inner-icon="
									visible ? 'mdi-eye-off' : 'mdi-eye'
								"
								:type="visible ? 'text' : 'password'"
								density="compact"
								placeholder="Введите свой пароль"
								prepend-inner-icon="mdi-lock-outline"
								variant="outlined"
								@click:append-inner="visible = !visible"
								clearable
								v-model="password"
								:readonly="loading"
								:rules="[required, passwordRules]"
							></v-text-field>

							<!-- <v-card
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
						</v-card> -->

							<v-btn
								block
								class="mb-8"
								color="blue"
								size="large"
								variant="tonal"
								:disabled="!form"
								:loading="loading"
								type="submit"
							>
								<strong>Войти</strong>
							</v-btn>

							<v-card-text class="text-center">
								<router-link
									:to="{ name: 'sign-up' }"
									replace
									style="text-decoration: none"
								>
									Зарегистрироваться
									<v-icon icon="mdi-chevron-right"></v-icon
								></router-link>
							</v-card-text>
						</v-form>
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
				form: false,
				username: null,
				password: null,
			}
		},

		methods: {
			async onSubmit(event) {
				if (!this.form) return
				try {
					this.loading = true
					await new Promise((resolve, reject) => {
						setTimeout(() => {
							this.loading = false
							resolve()
						}, 2000)
					})
				} catch (error) {
					console.log('ERROR')
				} finally {
					this.password = null
				}
			},
			required(v) {
				return !!v || 'Обязательное поле'
			},
			passwordRules(v) {
				return (
					(v && v.length >= 8) ||
					'Пароль должен быть больше 8 символов!'
				)
			},
			usernameRules(v) {},
		},
	}
</script>

<style scoped></style>
