<template>
	<v-form class="login-form" v-model="form" @submit.prevent="onSubmit">
		<div class="text-h4">Войти</div>
		<!-- <div class="text-subtitle-1">Логин</div> -->
		<div>
			<v-text-field
				autofocus
				density="compact"
				label="Имя пользователя"
				variant="outlined"
				v-model="username"
				:readonly="loading"
				:rules="[required, usernameRules]"
			></v-text-field>
		</div>
		<!-- <div class="text-subtitle-1">Пароль</div> -->
		<div>
			<v-text-field
				:append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
				:type="visible ? 'text' : 'password'"
				density="compact"
				label="Пароль"
				variant="outlined"
				@click:append-inner="visible = !visible"
				v-model="password"
				:readonly="loading"
				:rules="[required, passwordRules]"
			></v-text-field>
		</div>

		<div>
			<v-btn
				class="mb-12"
				variant="tonal"
				size="large"
				:disabled="!form"
				:loading="loading"
				type="submit"
			>
				<strong>Войти</strong>
			</v-btn>
		</div>
	</v-form>
</template>
<script>
	export default {
		name: 'login-form-widget',
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
					(v && v.length >= 4) ||
					'Пароль должен быть больше 4 символов!'
				)
			},
			usernameRules(v) {},
		},
	}
</script>

<style scoped>
	.login-form > div {
		margin-top: 10px;
	}
</style>
