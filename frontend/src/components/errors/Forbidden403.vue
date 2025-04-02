<template>
	<div class="container">
		<h1>{{ t('errors.notFound.code') }}</h1>
		<h2>{{ t('errors.notFound.title') }}</h2>
		<p>
			{{ t('errors.notFound.text') }}
		</p>
		<v-btn
			:color="t('errors.notFound.button.color')"
			class="btn"
			@click="goToHome()"
			>{{ t('errors.notFound.button.text') }}</v-btn
		>
	</div>
</template>

<script setup>
	import { useI18n } from 'vue-i18n'
	import { useRouter } from 'vue-router'
	const { t } = useI18n()
	const router = useRouter()

	const goToHome = async () => {
		await router.replace({
			name: 'home',
		})
	}
</script>

<style scoped>
	.container {
		margin-top: 100px;
	}
	.btn {
		padding: 8px 50px;
		border-radius: 30px;
		cursor: pointer;
		font-size: 1em;
		transition: 0.2s ease;
		font-weight: bold;
		margin: 5px 0px;
	}
	@media screen and (max-width: 768px) {
		body {
			display: block;
		}
		.container {
			margin-left: 40px;
			margin-top: 70px;
			margin-bottom: 70px;
		}
	}
</style>
