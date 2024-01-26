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
				<v-container>
					<v-hover>
						<template v-slot:default="{ isHovering, props }">
							<v-card
								v-bind="props"
								:color="isHovering ? 'primary' : undefined"
							>
								<v-card-title>
									<strong> {{ title }} </strong></v-card-title
								>
								<v-card-text> {{ text }}</v-card-text></v-card
							>
						</template>
					</v-hover>
				</v-container>
			</v-col>
		</v-row>
	</v-app>
</template>

<script lang="js">
	import { VAppBarNavIcon } from 'vuetify/lib/components/index.mjs'

	export default {
		name: 'home',
		components: { VAppBarNavIcon },
		data() {
			return {
				drawer: true,
				rail: true,
				title: 'Добро пожаловать на сайт!',
				text: `Мы рады приветствовать вас на платформе, посвященной отображению
				статистики нормативно-правовых актов по всей стране, включая информацию
				по округам и регионам. Здесь вы сможете удобно ознакомиться с ключевыми
				нормами, анализировать законодательные требования и отслеживать изменения
				в правовом поле.
				Наши инструменты предоставляют широкий обзор законодательства,
				позволяя вам легко навигировать по различным уровням власти и местам действия.
				Мы стремимся сделать процесс работы с нормативами максимально удобным и
				информативным.
				Не забывайте использовать доступные фильтры и инструменты
				аналитики для более глубокого понимания юридической среды в различных регионах.
				Если у вас есть вопросы или предложения, наша команда готова помочь вам
				получить максимум от использования нашего ресурса.
				Спасибо за выбор нашего сайта. Приятной работы!`,
			}
		},

		methods: {
			async goToDashboard() {
				await this.$router.push({
					name: 'dashboard',
				})
				console.log('go to Dashboard')
			},
		},
	}
</script>

<style scoped></style>
