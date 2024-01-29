<template>
	<v-app>
		<SignUpForm />
	</v-app>
</template>

<script lang="js">
	import { SignUpForm } from '../widget'
	export default {
		name: 'sign-up',
		components: { SignUpForm },
		data() {
			return {
				name: 'sign-up',
			}
		},
	}
</script>

<style scoped></style>
