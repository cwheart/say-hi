import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../composables/useAuth'

import AdminLogin from '../views/AdminLogin.vue'
import DashboardView from '../views/DashboardView.vue'
import UsersView from '../views/UsersView.vue'
import PracticesView from '../views/PracticesView.vue'
import PracticeFormView from '../views/PracticeFormView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: AdminLogin,
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      name: 'Dashboard',
      component: DashboardView,
    },
    {
      path: '/users',
      name: 'Users',
      component: UsersView,
    },
    {
      path: '/practices',
      name: 'Practices',
      component: PracticesView,
    },
    {
      path: '/practices/new',
      name: 'PracticeCreate',
      component: PracticeFormView,
    },
    {
      path: '/practices/:id/edit',
      name: 'PracticeEdit',
      component: PracticeFormView,
    },
    {
      path: '/history',
      name: 'History',
      component: HistoryView,
    },
  ],
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()

  if (to.meta.requiresAuth === false) {
    // Public route (login)
    if (isAuthenticated.value && to.path === '/login') {
      return '/'
    }
    return true
  }

  // Protected routes
  if (!isAuthenticated.value) {
    return '/login'
  }

  return true
})

export default router