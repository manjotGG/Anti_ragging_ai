<template>
  <div class="space-y-6">
    <div class="rounded-3xl border border-slate-200/80 bg-slate-50 p-6 shadow-soft dark:border-slate-700/80 dark:bg-slate-950/80">
      <div>
        <p class="text-sm uppercase tracking-[0.3em] text-indigo-600">Track complaint</p>
        <h2 class="mt-2 text-2xl font-semibold">Enter your tracking ID</h2>
      </div>

      <form @submit.prevent="loadStatus" class="grid gap-4 sm:grid-cols-[1fr_auto]">
        <input v-model="trackingId" placeholder="Tracking ID" class="w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-indigo-400 dark:focus:ring-indigo-900" />
        <button type="submit" class="rounded-3xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500">Check Status</button>
      </form>

      <p class="text-sm text-slate-500 dark:text-slate-400">Use the ID provided after complaint submission to check progress and resolution.</p>
    </div>

    <div v-if="error" class="rounded-3xl border border-red-200 bg-red-50 p-5 text-sm text-red-700 dark:border-red-700/40 dark:bg-red-950/40 dark:text-red-200">{{ error }}</div>

    <div v-if="statusResult" class="space-y-4 rounded-3xl border border-slate-200/80 bg-white p-6 shadow-soft dark:border-slate-700/80 dark:bg-slate-950/90">
      <div class="flex items-center justify-between gap-4">
        <div>
          <p class="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Current status</p>
          <p class="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">{{ statusResult.status }}</p>
        </div>
        <span :class="statusBadge(statusResult.status)">{{ statusResult.status }}</span>
      </div>

      <div class="grid gap-4 sm:grid-cols-2">
        <div class="rounded-3xl bg-slate-50 p-5 dark:bg-slate-900">
          <p class="text-sm text-slate-500 dark:text-slate-400">Tracking ID</p>
          <p class="mt-2 font-semibold text-slate-900 dark:text-slate-100">{{ statusResult.tracking_id }}</p>
        </div>
        <div class="rounded-3xl bg-slate-50 p-5 dark:bg-slate-900">
          <p class="text-sm text-slate-500 dark:text-slate-400">Reported At</p>
          <p class="mt-2 font-semibold text-slate-900 dark:text-slate-100">{{ formattedDate }}</p>
        </div>
      </div>

      <div class="rounded-3xl bg-slate-50 p-5 dark:bg-slate-900">
        <p class="text-sm text-slate-500 dark:text-slate-400">Description</p>
        <p class="mt-3 text-slate-700 dark:text-slate-200 whitespace-pre-line">{{ statusResult.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'
const trackingId = ref('')
const statusResult = ref(null)
const error = ref('')

const formattedDate = computed(() => {
  if (!statusResult.value?.created_at) return '-'
  return new Date(statusResult.value.created_at).toLocaleString()
})

function statusBadge(status) {
  return status === 'resolved'
    ? 'rounded-full bg-emerald-500 px-3 py-1 text-xs font-semibold text-white'
    : 'rounded-full bg-amber-500 px-3 py-1 text-xs font-semibold text-slate-950'
}

async function loadStatus() {
  error.value = ''
  statusResult.value = null
  const id = trackingId.value.trim()
  if (!id) {
    error.value = 'Please enter a valid tracking ID.'
    return
  }

  try {
    const response = await axios.get(`${API_BASE}/status/${encodeURIComponent(id)}`)
    if (response.data.error) {
      error.value = response.data.error
    } else {
      statusResult.value = response.data
    }
  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'Unable to load complaint status.'
  }
}
</script>
