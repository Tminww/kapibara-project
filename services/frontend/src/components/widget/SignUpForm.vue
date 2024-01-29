<template>
	<div class="d-flex align-center justify-center" style="height: 100vh">
		<v-sheet width="400" class="mx-auto">
			<v-form fast-fail @submit.prevent="signup">
				<v-text-field
					variant="underlined"
					v-model="name"
					label="Name"
				></v-text-field>
				<v-text-field
					variant="underlined"
					v-model="email"
					label="Email"
				></v-text-field>
				<v-text-field
					variant="underlined"
					v-model="password"
					label="password"
				></v-text-field>

				<v-btn type="submit" color="primary" block class="mt-2"
					>Sign up</v-btn
				>
			</v-form>
			<div class="mt-2">
				<p class="text-body-2">
					Already have an account?
					<router-link :to="{ name: 'login' }">
						Login <v-icon icon="mdi-chevron-right"></v-icon
					></router-link>
				</p>
			</div>
		</v-sheet>
	</div>
</template>
<script>
	export default {
		data() {
			return {
				name: '',
				email: '',
				password: '',
			}
		},
		methods: {
			signup() {
				//
			},
		},
	}
</script>
