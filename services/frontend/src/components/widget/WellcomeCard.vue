<template>
	<v-container>
		<v-hover v-slot="{ isHovering }">
			<v-card>
				<v-card-title>
					<strong>Welcome to Our Site!</strong>
				</v-card-title>
				<v-card-text>
					We are glad to see you here! Please explore our website and
					find out more about us and our services.
				</v-card-text>
			</v-card>
		</v-hover>
	</v-container>
</template>

<script lang="js">
	export default {
		name: 'welcome-card',
		data() {
			return {}
		},
	}
</script>

<style scoped></style>
