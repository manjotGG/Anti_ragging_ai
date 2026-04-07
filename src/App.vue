<template>
  <div class="min-h-screen bg-slate-50 px-4 py-6 transition-colors duration-300 ease-in-out dark:bg-slate-950 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <header class="flex flex-col gap-4 rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-soft backdrop-blur transition-colors duration-300 dark:border-slate-700/80 dark:bg-slate-900/95">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.3em] text-indigo-600">AI Anti-Ragging</p>
            <h1 class="mt-3 text-3xl font-semibold sm:text-4xl">Student Safety & Complaint Tracker</h1>
            <p class="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
              Submit complaints by text or voice, track status with a secure ID, and manage reports through secure admin access.
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <ThemeToggle />
            <button v-if="auth.state.token" @click="handleLogout" class="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-800 shadow-sm transition duration-300 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700">
              Logout
            </button>
            <router-link v-else to="/admin/login" class="inline-flex items-center rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-800 shadow-sm transition duration-300 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700">
              Admin Login
            </router-link>
          </div>
        </div>

        <nav class="grid gap-3 sm:grid-cols-2">
          <router-link :to="{ name: 'Home' }" :class="navClass('Home')">Home</router-link>
          <router-link v-if="auth.state.token" :to="{ name: 'AdminDashboard' }" :class="navClass('AdminDashboard')">Admin Dashboard</router-link>
        </nav>
      </header>

      <main class="mt-8">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ThemeToggle from './components/ThemeToggle.vue'
import auth from './store/auth'

const router = useRouter()
const route = useRoute()

const navClass = (routeName) => {
  const active = 'rounded-2xl px-4 py-3 text-sm font-medium bg-indigo-600 text-white shadow-sm'
  const inactive = 'rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700'
  return route.name === routeName ? active : inactive
}

function handleLogout() {
  auth.logout()
  router.push({ name: 'Home' })
}
</script>
