import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import PracticeList from '../views/PracticeList.vue'
import PracticeDetail from '../views/PracticeDetail.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HistoryList from '../views/HistoryList.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { public: true },
    },
    {
      path: '/',
      name: 'practice-list',
      component: PracticeList,
    },
    {
      path: '/practice/:id',
      name: 'practice-detail',
      component: PracticeDetail,
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryList,
    },
  ],
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const { isAuthenticated } = useAuth()

  if (!to.meta.public && !isAuthenticated.value) {
    next('/login')
  } else if ((to.name === 'login' || to.name === 'register') && isAuthenticated.value) {
    next('/')
  } else {
    next()
  }
})

export default router