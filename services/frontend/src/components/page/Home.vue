<template>
	<v-row>
		<v-col>
			<v-container>
				<v-navigation-drawer
					location="left"
					temporary
					:width="500"
					v-model="drawer"
					:rail="rail"
					permanent
					@click="rail = false"
				>
					<v-list-item
						prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
						title="John Leider"
						nav
					>
						<template v-slot:append>
							<v-btn
								variant="text"
								icon="mdi-chevron-left"
								@click.stop="rail = !rail"
							></v-btn>
						</template>
					</v-list-item>

					<v-divider></v-divider>

					<v-list density="compact" nav>
						<v-list-item
							prepend-icon="mdi-view-dashboard"
							title="Dashboard"
						></v-list-item>
					</v-list>
				</v-navigation-drawer>
			</v-container>
		</v-col>
	</v-row>

	<v-hover>
		<template v-slot:default="{ isHovering, props }">
			<v-card
				v-bind="props"
				:color="isHovering ? 'primary' : undefined"
				title="Hover over me"
				text="..."
			></v-card>
		</template>
	</v-hover>
</template>

<script lang="js">
	export default {
		name: 'home',
		components: {},
		data() {
			return {
				drawer: true,
				rail: true,
			}
		},
	}
</script>

<style scoped></style>
