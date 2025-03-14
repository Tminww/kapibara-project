<template>
	<t-header-widget :color="t('layouts.dashboard.header.color')">
		<template #title>
			<div @click="goToHome()">
				{{ t('layouts.dashboard.header.title') }}
			</div>
		</template>

		<!-- <template #login>
			<div
				v-if="authData.token === null"
				@click="goToLogin()"
				variant="plain"
				:ripple="false"
			>
				{{ t('layouts.dashboard.header.login') }}
			</div>
			<div
				v-else=""
				@click="goToLogout()"
				variant="plain"
				:ripple="false"
			>
				({{ authData.username }})
				{{ t('layouts.dashboard.header.logout') }}
			</div>
		</template> -->
	</t-header-widget>

	<v-main>
		<v-row no-gutters class="justify-start">
			<v-col>
				<v-container fluid>
					<t-breadcrumbs
						v-if="route.name !== 'home'"
						divider="/"
					></t-breadcrumbs
				></v-container>
			</v-col>
		</v-row>

		<slot></slot>
	</v-main>

	<Toaster richColors :expand="true" position="bottom-right" />
</template>

<script setup>
	import { THeaderWidget, TBreadcrumbs } from '@/components/widgets'
	import { Toaster } from 'vue-sonner'
	import { getAuthDataFromLocalStorage } from '@/utils/auth'
	import { computed } from 'vue'
	import { useRouter, useRoute } from 'vue-router'
	import { useI18n } from 'vue-i18n'

	const router = useRouter()
	const route = useRoute()
	const { t } = useI18n()

	const authData = computed(() => {
		console.log(getAuthDataFromLocalStorage())
		return getAuthDataFromLocalStorage()
	})

	const breadcrumbs = [
		{
			text: 'Главная',
			disabled: false,
			href: 'home',
		},
	]

	const goToLogin = async () => {
		await router.push({
			name: 'login',
		})
	}

	const goToLogout = async () => {
		localStorage.clear()

		await router.replace({
			name: 'home',
		})
		// Вызывается для того, чтобы очистить хранилище vuex,
		// считать данные из localStorage и заново отрендерить layout
		window.location.reload()
	}

	const goToHome = async () => {
		await router.push({
			name: 'home',
		})
	}
</script>

<style scoped></style>
