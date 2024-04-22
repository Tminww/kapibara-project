<template>
	<v-app>
		<LoginForm />
		<router-view></router-view>
	</v-app>
</template>

<script lang="js">
	import { LoginForm } from '../widget'
	export default {
		name: 'login',
		components: { LoginForm },
		data() {
			return {
				name: 'login',
			}
		},
		methods: {
			async goToSignUp() {
				await this.$router.push({
					name: 'sign-up',
				})
				console.log('go to SignUp')
			},
		},
	}
</script>

<style scoped></style>
