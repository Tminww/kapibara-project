<template>
	<v-container class="mt-15">
		<v-row class="d-flex align-center">
			<v-col>
				<v-container width="500">
					<t-error-icon-ui></t-error-icon-ui>
				</v-container>
			</v-col>
			<v-col>
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
	svg .dark {
		stroke: var(--color-ui-bg-primary);
	}

	svg .fill-dark {
		fill: var(--color-ui-bg-primary);
	}

	svg .fill-light {
		fill: var(--color-ui-bg-inverted);
	}

	@media screen and (max-width: 768px) {
		main {
			display: block;
		}

		.picture,
		.content {
			width: 100%;
			text-align: center;
		}

		.content {
			padding: 0 20px;
		}

		.picture svg {
			max-width: 100%;
		}
	}

	@keyframes moveAndRotate {
		0% {
			transform: translateY(0) rotate(0);
		}
		50% {
			transform: translateY(1px) rotate(1deg);
		}
		100% {
			transform: translateY(0) rotate(0);
		}
	}

	svg #spaceman {
		animation: moveAndRotate 2.5s ease-in-out infinite alternate;
	}

	@keyframes moveXLeft {
		0%,
		100% {
			transform: translateX(0);
		}
		50% {
			transform: translateX(-3px);
		}
	}

	svg #craterSmall {
		animation: moveXLeft 1.7s ease-in-out infinite alternate;
	}

	@keyframes moveXRight {
		0%,
		100% {
			transform: translateX(0);
		}
		50% {
			transform: translateX(3px);
		}
	}

	svg #craterBig {
		animation: moveXRight 2s ease-in-out infinite alternate;
	}

	@keyframes rotatePlanet {
		0%,
		100% {
			transform: rotate(0);
		}
		50% {
			transform: rotate(-2deg);
		}
	}

	svg #planet {
		animation: rotatePlanet 2.2s ease-in-out infinite alternate;
		transform-origin: 70% 30%;
	}

	@keyframes rotateStars {
		0%,
		100% {
			transform: rotate(0);
		}
		50% {
			transform: rotate(calc(0.8deg));
		}
	}

	svg #starsBig g {
		animation: rotateStars 1s ease-in-out infinite alternate;
		transform-origin: 40% 60%;
	}

	@keyframes scaleStars {
		0% {
			transform: scale(0.96);
		}
		50% {
			transform: scale(1);
		}
		100% {
			transform: scale(0.98);
		}
	}

	svg #starsSmall g {
		animation: scaleStars 1.7s ease-in-out infinite alternate;
		transform-origin: 50% 50%;
	}

	@keyframes moveYSmall {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-4px);
		}
	}

	svg #circlesSmall circle {
		animation: moveYSmall 1.85s ease-in-out infinite alternate;
	}

	@keyframes moveYBig {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-3px);
		}
	}

	svg #circlesBig circle {
		animation: moveYBig 2s ease-in-out infinite alternate;
	}

	svg #glassShine {
		opacity: 0;
	}
</style>
