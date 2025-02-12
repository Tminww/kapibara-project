import { createRouter, createWebHistory } from 'vue-router'

import dashboardRoutes from './dashboardRoutes'
import errorRoutes from './errorRoutes'
import homeRoutes from './homeRoutes'
import authRoutes from './authRoutes'

const routes = [
	...homeRoutes,
	...authRoutes,
	...dashboardRoutes,
	...errorRoutes,
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
