import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboardView from '../views/AdminDashboard.vue'
import auth from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin,
    meta: { guestOnly: true },
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboardView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = auth.isAuthenticated()

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'AdminLogin' })
    return
  }

  if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'AdminDashboard' })
    return
  }

  next()
})

export default router
