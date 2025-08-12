import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'

import { routes as dashboardRoutes } from '@/components/dashboard/router'
import { routes as subjectRoutes } from '@/components/subjects/router'

import stateStorage from '@/utils/auth'

const meta = {
  requiresAuth: false,
  forAdmin: false,
  forUser: false,
  forAll: true
}

const routes = [
  ...dashboardRoutes,
  ...subjectRoutes,
  { path: '/login', name: 'login', component: () => import('@/components/login/LoginPage.vue') },
  {
    path: '/parser',
    name: 'parser',
    component: () => import('@/components/parser/ParserInfoPage.vue'),
    meta: {
      requiresAuth: true,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Информационная панель сбора данных'
        }
      ]
    }
  },
  {
    path: '/validator',
    name: 'validator',
    component: () => import('@/components/validator/ValidatorInfoPage.vue'),
    meta: {
      requiresAuth: true,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Информационная панель проверки данных'
        }
      ]
    }
  },
  {
    path: '/root',
    name: 'home',
    component: () => import('@/components/home/HomePage.vue')
  },
  {
    path: '/president',
    name: 'president',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Президент'
        }
      ]
    }
  },
  {
    path: '/council_1',
    name: 'council_1',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Совет Федерации'
        }
      ]
    }
  },
  {
    path: '/council_2',
    name: 'council_2',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Государственная Дума'
        }
      ]
    }
  },
  {
    path: '/government',
    name: 'government',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Правительство'
        }
      ]
    }
  },
  {
    path: '/federal_authorities',
    name: 'federal_authorities',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'ФОИВ и ФГО'
        }
      ]
    }
  },
  {
    path: '/court',
    name: 'court',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Конституционный Суд'
        }
      ]
    }
  },
  {
    path: '/international',
    name: 'international',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Международные договоры'
        }
      ]
    }
  },
  {
    path: '/un_securitycouncil',
    name: 'un_securitycouncil',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta: {
      ...meta,
      breadCrumb: [
        {
          text: 'Главная',
          to: { name: 'home' }
        },
        {
          text: 'Совет Безопасности ООН'
        }
      ]
    }
  },
  {
    path: '/table',
    name: 'table',
    component: () => import('@/components/table/TablePage.vue')
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/components/errors/NotFound404.vue'),
    meta
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from) => {
  // Если маршрут доступен для всех, пропускаем его без редиректа

  // Если маршрут требует авторизации, но пользователь не авторизован
  if (to.meta.requiresAuth && stateStorage.value.token === '') {
    // Предотвращаем цикл перенаправлений на страницу входа
    if (to.name !== 'login') {
      return {
        name: 'login',
        query: { redirect: to.name as string }
      }
    }
  }

  // Разрешаем переход, если все условия выполнены
  return true
})

export default router
