<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 rounded-3xl border border-slate-200/80 bg-slate-50 p-6 shadow-soft dark:border-slate-700/80 dark:bg-slate-950/80 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-sm uppercase tracking-[0.3em] text-indigo-600">Admin panel</p>
        <h2 class="mt-2 text-2xl font-semibold">Manage complaints</h2>
      </div>
      <input v-model="searchQuery" placeholder="Search complaints" class="w-full max-w-md rounded-3xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-indigo-400 dark:focus:ring-indigo-900" />
    </div>

    <div class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft dark:border-slate-700 dark:bg-slate-950">
      <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
        <thead class="bg-slate-100 text-left text-xs uppercase tracking-[0.3em] text-slate-600 dark:bg-slate-900 dark:text-slate-400">
          <tr>
            <th class="px-4 py-4">Tracking ID</th>
            <th class="px-4 py-4">Severity</th>
            <th class="px-4 py-4">Status</th>
            <th class="px-4 py-4">Accused</th>
            <th class="px-4 py-4">Description</th>
            <th class="px-4 py-4">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 bg-white dark:divide-slate-800 dark:bg-slate-950">
          <tr v-for="complaint in filteredComplaints" :key="complaint.tracking_id" class="hover:bg-slate-50 dark:hover:bg-slate-900">
            <td class="px-4 py-4 text-sm font-semibold text-slate-900 dark:text-slate-100">{{ complaint.tracking_id }}</td>
            <td class="px-4 py-4">
              <span :class="severityBadge(complaint.severity)">{{ complaint.severity }}</span>
            </td>
            <td class="px-4 py-4">
              <span :class="statusBadge(complaint.status)">{{ complaint.status }}</span>
            </td>
            <td class="px-4 py-4 text-sm text-slate-700 dark:text-slate-300">{{ complaint.accused_name || 'N/A' }}</td>
            <td class="px-4 py-4 text-sm text-slate-700 dark:text-slate-300">{{ complaint.description }}</td>
            <td class="px-4 py-4">
              <button @click="closeComplaint(complaint.tracking_id)" :disabled="complaint.status === 'resolved'" class="rounded-full px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-40" :class="complaint.status === 'resolved' ? 'bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-400' : 'bg-emerald-600 text-white hover:bg-emerald-500'">Close शिकायत</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid gap-4 sm:grid-cols-2">
      <div class="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-300">
        <p class="font-semibold text-slate-900 dark:text-slate-100">Total complaints</p>
        <p class="mt-2 text-3xl font-bold">{{ complaints.length }}</p>
      </div>
      <div class="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-300">
        <p class="font-semibold text-slate-900 dark:text-slate-100">Open reports</p>
        <p class="mt-2 text-3xl font-bold">{{ openCount }}</p>
      </div>
    </div>

    <div v-if="toast.message" :class="toastClass" class="rounded-3xl p-4 text-sm font-medium transition">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'

import auth from '../store/auth'

const API_BASE = 'http://127.0.0.1:8000'
const complaints = ref([])
const searchQuery = ref('')
const toast = reactive({ message: '', type: 'info' })

const filteredComplaints = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) return complaints.value
  return complaints.value.filter((item) => {
    return [
      item.tracking_id,
      item.description,
      item.accused_name,
      item.severity,
      item.status,
    ]
      .filter(Boolean)
      .some((value) => value.toLowerCase().includes(query))
  })
})

const openCount = computed(() => complaints.value.filter((item) => item.status !== 'resolved').length)

const toastClass = computed(() => {
  if (toast.type === 'success') return 'bg-emerald-600 text-white'
  if (toast.type === 'error') return 'bg-red-600 text-white'
  return 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100'
})

function severityBadge(severity) {
  if (severity === 'high') return 'rounded-full bg-red-600 px-3 py-1 text-xs font-semibold text-white'
  if (severity === 'medium') return 'rounded-full bg-amber-500 px-3 py-1 text-xs font-semibold text-slate-950'
  return 'rounded-full bg-emerald-500 px-3 py-1 text-xs font-semibold text-white'
}

function statusBadge(status) {
  return status === 'resolved'
    ? 'rounded-full bg-emerald-500 px-3 py-1 text-xs font-semibold text-white'
    : 'rounded-full bg-amber-500 px-3 py-1 text-xs font-semibold text-slate-950'
}

function showToast(message, type = 'info') {
  toast.message = message
  toast.type = type
  setTimeout(() => {
    toast.message = ''
  }, 3200)
}

async function loadComplaints() {
  try {
    const response = await axios.get(`${API_BASE}/admin/complaints`, {
      headers: {
        Authorization: `Bearer ${auth.state.token}`,
      },
    })
    complaints.value = response.data.complaints || []
  } catch (error) {
    showToast('Unable to load complaints. Check admin login and backend.', 'error')
  }
}

async function closeComplaint(trackingId) {
  try {
    const response = await axios.put(`${API_BASE}/admin/close/${encodeURIComponent(trackingId)}`, null, {
      headers: {
        Authorization: `Bearer ${auth.state.token}`,
      },
    })
    if (response.data.error) {
      showToast(response.data.error, 'error')
      return
    }
    const complaint = complaints.value.find((item) => item.tracking_id === trackingId)
    if (complaint) complaint.status = 'resolved'
    showToast('Complaint marked as resolved.', 'success')
  } catch (error) {
    showToast('Close request failed. Try again.', 'error')
  }
}

onMounted(() => {
  loadComplaints()
})
</script>
