<template>
	<nav class="breadcrumbs-container pl-0">
		<ul class="breadcrumbs-list">
			<li
				v-for="(item, index) in breadCrumbs"
				:key="index"
				class="breadcrumb-item"
			>
				<router-link
					v-if="item.to"
					:to="item.to"
					class="breadcrumb-link"
				>
					{{ item.text }}
				</router-link>
				<span v-else class="breadcrumb-text font-weight-bold">
					{{ item.text }}
				</span>
				<span
					v-if="index < breadCrumbs.length - 1"
					class="breadcrumb-divider"
					>{{ props.divider }}</span
				>
			</li>
		</ul>
	</nav>
</template>

<script setup>
	import { computed, defineProps } from 'vue'
	import { useRoute } from 'vue-router'

	// Принимаем пропсы
	const props = defineProps({
		divider: {
			type: String,
			default: '/',
		},
	})

	// Вычисляем хлебные крошки из route.meta или пропсов
	const route = useRoute()
	const breadCrumbs = computed(() => {
		if (typeof route.meta.breadCrumb === 'function') {
			return route.meta.breadCrumb.call(this, route)
		}
		return route.meta.breadCrumb || []
	})
	console.log('BreadCrumbs:', breadCrumbs.value)
</script>

<style scoped>
	/* Контейнер навигации */
	.breadcrumbs-container {
		padding: 8px 16px;
		width: 100%;
		box-sizing: border-box;
	}

	/* Список хлебных крошек */
	.breadcrumbs-list {
		display: flex;
		flex-wrap: wrap; /* Разрешаем перенос элементов */
		gap: 4px; /* Расстояние между элементами */
		list-style: none;
		margin: 0;
		padding: 0;
	}

	/* Каждый элемент списка */
	.breadcrumb-item {
		display: flex;
		align-items: center;
		margin: 0;
	}

	/* Ссылка */
	.breadcrumb-link {
		text-decoration: none;
		color: #1976d2; /* Цвет ссылки по умолчанию (можно настроить) */
		font-size: 14px;
		overflow-wrap: break-word; /* Перенос длинных слов */
		word-break: break-all; /* Дополнительная поддержка переноса */
		max-width: 100%; /* Ограничиваем ширину текста */
		white-space: normal; /* Разрешаем перенос строк */
	}

	.breadcrumb-link:hover {
		text-decoration: underline;
	}

	/* Текст без ссылки (например, текущая страница) */
	.breadcrumb-text {
		font-size: 14px;
		overflow-wrap: break-word;
		word-break: break-all;
		max-width: 100%;
		white-space: normal;
	}

	/* Разделитель */
	.breadcrumb-divider {
		margin: 0 4px;
		color: gray;
		font-size: 14px;
	}

	/* Адаптивность для мобильных устройств */
	@media (max-width: 600px) {
		.breadcrumbs-container {
			padding: 4px 8px; /* Меньше отступов на мобильных */
			flex-direction: row; /* Вертикальная компоновка */
			align-items: flex-start;
		}

		.breadcrumbs-list {
			flex-direction: row;
			gap: 2px; /* Меньше расстояние между элементами */
		}

		.breadcrumb-item {
			width: 100%;
			margin-bottom: 2px;
		}
	}
</style>
