<template>
	<v-container class="mt-15">
		<v-row class="d-flex align-center">
			<v-col cols="auto">
				<v-container width="500">
					<t-error-icon-ui></t-error-icon-ui>
				</v-container>
			</v-col>
			<v-col cols="auto">
				<v-container width="400">
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
				</v-container>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { useI18n } from 'vue-i18n'
	import { useRouter } from 'vue-router'
	import { TErrorIconUi } from '@/components/ui'

	const { t } = useI18n()
	const router = useRouter()

	const goToHome = async () => {
		await router.replace({
			name: 'home',
		})
	}
</script>

<style scoped>
	.error-container {
		display: flex;
		align-items: center; /* Центрирование по вертикали */
		justify-content: center; /* Можно заменить на space-between, если нужно больше пространства */
		gap: 20px; /* Пространство между изображением и текстом */
		width: 100%;
		max-width: 900px;
		margin: 0 auto;
	}

	.picture {
		width: 120%; /* Задаем ширину изображения */
		display: flex;
		justify-content: center;
	}

	.content {
		width: 100%; /* Ширина блока с текстом */
		/* padding: 0 20px; */
	}

	/* Для мобильных устройств делаем вертикальное расположение */
	@media screen and (max-width: 768px) {
		.error-container {
			flex-direction: column;
			text-align: center;
		}

		.picture,
		.content {
			width: 100%;
		}
	}

	.error-container {
		margin-top: 100px;
		display: flex;
		flex-direction: row;
	}
	.btn {
		/* padding: 8px 50px; */
		border-radius: 30px;
		cursor: pointer;
		font-size: 1em;
		transition: 0.2s ease;
		font-weight: bold;
		margin: 15px 0px;
	}
	@media screen and (max-width: 768px) {
		body {
			display: block;
		}
		.error-container {
			margin-left: 40px;
			margin-top: 70px;
			margin-bottom: 70px;
		}
	}
</style>
