<template>
  <div class="mx-auto max-w-xl rounded-3xl border border-slate-200 bg-white/95 p-8 shadow-soft transition duration-300 dark:border-slate-700 dark:bg-slate-900/95">
    <h1 class="text-3xl font-semibold text-slate-900 dark:text-slate-100">Admin Sign In</h1>
    <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">Secure admin access to manage complaints.</p>

    <form @submit.prevent="handleLogin" class="mt-8 space-y-5">
      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-200">Username</label>
        <input v-model="username" type="text" autocomplete="username" placeholder="admin" class="mt-2 w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-indigo-400 dark:focus:ring-indigo-900" />
      </div>

      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-200">Password</label>
        <input v-model="password" type="password" autocomplete="current-password" placeholder="••••••••" class="mt-2 w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-indigo-400 dark:focus:ring-indigo-900" />
      </div>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <button type="submit" :disabled="auth.state.loading" class="inline-flex items-center justify-center rounded-3xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50">
          <span v-if="auth.state.loading">Signing in…</span>
          <span v-else>Login</span>
        </button>
      </div>

      <p v-if="auth.state.error" class="rounded-3xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-700/40 dark:bg-red-950/40 dark:text-red-200">{{ auth.state.error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import auth from '../store/auth'

const router = useRouter()
const username = ref('')
const password = ref('')

async function handleLogin() {
  const success = await auth.login(username.value.trim(), password.value)
  if (success) {
    router.push({ name: 'AdminDashboard' })
  }
}
</script>
