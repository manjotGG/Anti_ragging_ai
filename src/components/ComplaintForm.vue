<template>
  <div class="space-y-6">
    <div class="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
      <div class="space-y-4 rounded-3xl border border-slate-200/80 bg-slate-50 p-6 shadow-soft dark:border-slate-700/80 dark:bg-slate-950/80">
        <div>
          <p class="text-sm uppercase tracking-[0.3em] text-indigo-600">Make a report</p>
          <h2 class="mt-2 text-2xl font-semibold">Submit your complaint</h2>
          <p class="mt-2 text-slate-600 dark:text-slate-300">Enter details below or use voice input to file a complaint quickly.</p>
        </div>

        <div class="space-y-3">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-200">Complaint description</label>
          <textarea v-model="complaint" rows="7" placeholder="Describe the incident in as much detail as possible" class="w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-indigo-400 dark:focus:ring-indigo-900"></textarea>
        </div>

        <VoiceInput @transcript="onTranscript" />

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div class="space-y-1">
            <p class="text-sm text-slate-500 dark:text-slate-400">Backend endpoint</p>
            <p class="text-sm font-semibold text-slate-700 dark:text-slate-200">POST /report</p>
          </div>
          <button @click="submitComplaint" :disabled="isLoading || !complaint.trim()" class="inline-flex items-center justify-center rounded-full bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50">
            <span v-if="isLoading" class="mr-2">Submitting…</span>
            <span v-else>Send Report</span>
          </button>
        </div>

        <p v-if="formError" class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-700/40 dark:bg-red-950/40 dark:text-red-200">{{ formError }}</p>
      </div>

      <div class="space-y-4 rounded-3xl border border-slate-200/80 bg-white p-6 shadow-soft dark:border-slate-700/80 dark:bg-slate-950/90">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">AI analysis</p>
            <h2 class="mt-2 text-xl font-semibold">Instant response</h2>
          </div>
          <div class="inline-flex items-center gap-2 rounded-full bg-slate-100 px-3 py-2 text-sm text-slate-600 shadow-sm dark:bg-slate-800 dark:text-slate-300">
            <span class="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
            Live feedback
          </div>
        </div>

        <div class="grid gap-4">
          <div v-if="reportResult" class="space-y-4 rounded-3xl border border-slate-200/80 bg-slate-50 p-5 dark:border-slate-700/80 dark:bg-slate-900/90">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p class="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Tracking ID</p>
                <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ reportResult.tracking_id }}</p>
              </div>
              <span :class="severityBadge(reportResult.severity)">{{ reportResult.severity }}</span>
            </div>

            <div class="grid gap-3 sm:grid-cols-2">
              <div class="rounded-3xl bg-white p-4 shadow-sm dark:bg-slate-950">
                <p class="text-sm text-slate-500 dark:text-slate-400">Category</p>
                <p class="mt-2 font-semibold text-slate-900 dark:text-slate-100">{{ reportResult.category }}</p>
              </div>
              <div class="rounded-3xl bg-white p-4 shadow-sm dark:bg-slate-950">
                <p class="text-sm text-slate-500 dark:text-slate-400">Emotion</p>
                <p class="mt-2 font-semibold text-slate-900 dark:text-slate-100">{{ reportResult.emotion }}</p>
              </div>
            </div>

            <p class="rounded-3xl bg-indigo-50 px-4 py-4 text-sm text-slate-700 dark:bg-indigo-950/40 dark:text-slate-200">{{ reportResult.support_message }}</p>
          </div>

          <div v-else class="rounded-3xl border border-dashed border-slate-300 p-6 text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
            Submit a complaint to view the AI classification, severity, and support response here.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import VoiceInput from './VoiceInput.vue'

const complaint = ref('')
const reportResult = ref(null)
const isLoading = ref(false)
const formError = ref('')
const API_BASE = 'http://127.0.0.1:8000'

function onTranscript(text) {
  complaint.value = text
}

function severityBadge(severity) {
  if (severity === 'high') return 'rounded-full bg-red-600 px-3 py-1 text-xs font-semibold text-white'
  if (severity === 'medium') return 'rounded-full bg-amber-500 px-3 py-1 text-xs font-semibold text-slate-950'
  return 'rounded-full bg-emerald-500 px-3 py-1 text-xs font-semibold text-white'
}

async function submitComplaint() {
  formError.value = ''
  reportResult.value = null
  const payload = complaint.value.trim()
  if (!payload) {
    formError.value = 'Please add a complaint description before submitting.'
    return
  }

  isLoading.value = true
  try {
    const response = await axios.post(`${API_BASE}/report`, { description: payload })
    reportResult.value = response.data
    complaint.value = ''
  } catch (error) {
    formError.value = error.response?.data?.error || error.message || 'Submission failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
