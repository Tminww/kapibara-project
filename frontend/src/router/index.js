import { createRouter, createWebHistory } from 'vue-router'
import { NotFound404 } from '@/pages/errors'
import { HomePage, LoginPage, SubjectPage } from '@/pages'

import { routes as dashboardRoutes } from '@/features/dashboard/router'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

const routes = [
	...dashboardRoutes,
	{
		path: '/',
		name: 'home',
		component: HomePage,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: '',
				},
			],
		},
	},

	{
		path: '/subjects',
		name: 'subjects',
		component: SubjectPage,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Субъекты',
				},
			],
		},
	},
	{
		path: '/subjects/district/:label',
		name: 'district',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Субъекты',
					to: { name: 'subjects' },
				},
				{
					text: '',
				},
			],
		},
		beforeEnter: (to, from, next) => {
			// Устанавливаем значение label в meta.breadCrumb
			to.meta.breadCrumb[2].text = to.params.label
			next()
		},
	},
	{
		path: '/president',
		name: 'president',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Президент',
				},
			],
		},
	},
	{
		path: '/council_1',
		name: 'council_1',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Совет Федерации',
				},
			],
		},
	},
	{
		path: '/council_2',
		name: 'council_2',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Государственная Дума',
				},
			],
		},
	},
	{
		path: '/government',
		name: 'government',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Правительство',
				},
			],
		},
	},
	{
		path: '/federal_authorities',
		name: 'federal_authorities',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'ФОИВ и ФГО',
				},
			],
		},
	},
	{
		path: '/court',
		name: 'court',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Конституционный Суд',
				},
			],
		},
	},
	{
		path: '/international',
		name: 'international',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Международные договоры',
				},
			],
		},
	},
	{
		path: '/un_securitycouncil',
		name: 'un_securitycouncil',
		component: NotFound404,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Совет Безопасности ООН',
				},
			],
		},
	},

	{
		path: '/:pathMatch(.*)*',
		name: 'not-found',
		component: NotFound404,
		meta,
	},
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from) => {
	const isLoggedIn = localStorage.getItem('token')
	const isAdmin = localStorage.getItem('role') === 'администратор'

	// Если маршрут доступен для всех, пропускаем его без редиректа
	if (to.meta.forAll) {
		return true
	}

	// Если маршрут требует авторизации, но пользователь не авторизован
	if (to.meta.requiresAuth && !isLoggedIn) {
		// Предотвращаем цикл перенаправлений на страницу входа
		if (to.name !== 'login') {
			return {
				name: 'login',
				query: { returnPage: to.name },
			}
		}
	}

	// Если маршрут только для администратора, но пользователь не админ
	if (to.meta.forAdmin && !isAdmin) {
		// Предотвращаем цикл перенаправлений на страницу 403
		if (to.name !== 'forbidden') {
			return {
				name: 'forbidden',
			}
		}
	}

	// Если маршрут только для обычных пользователей, но пользователь админ
	if (to.meta.forUser && isAdmin) {
		// Предотвращаем цикл перенаправлений на страницу 403
		if (to.name !== 'forbidden') {
			return {
				name: 'forbidden',
			}
		}
	}

	// Разрешаем переход, если все условия выполнены
	return true
})

export default router
