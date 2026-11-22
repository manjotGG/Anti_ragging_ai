<template>
  <div class="form-content">
    <p class="eyebrow">FOLLOW YOUR CONCERN</p>
    <h2 class="section-title">A little peace of mind.</h2>
    <p class="section-description">Enter the tracking ID you received when you submitted your report.</p>
    <form @submit.prevent="loadStatus" class="tracking-form" :aria-busy="isLoading">
      <label for="tracking-id">Tracking ID</label>
      <div class="tracking-input-row"><input id="tracking-id" v-model="trackingId" autocomplete="off" spellcheck="false" maxlength="8" placeholder="e.g. a1b2c3d4" required :aria-invalid="Boolean(error)" :aria-describedby="error ? 'tracking-help tracking-error' : 'tracking-help'" /><button type="submit" class="primary-button" :disabled="isLoading"><span v-if="isLoading" class="spinner" aria-hidden="true"></span><AppIcon v-else name="search" />{{ isLoading ? 'Checking…' : 'Check status' }}</button></div>
      <p id="tracking-help" class="small-note">Keep your ID private. Anyone with it can view your report.</p>
    </form>
    <p v-if="error" id="tracking-error" role="alert" class="feedback feedback-error"><AppIcon name="info" /><span>{{ error }}</span></p>
    <div v-if="statusResult" class="status-result" role="status" aria-live="polite">
      <div class="status-heading"><div><p class="eyebrow">CURRENT STATUS</p><h3>{{ statusResult.status === 'resolved' ? 'Your report is resolved' : 'Your report is with the team' }}</h3></div><span class="status-badge">{{ statusResult.status }}</span></div>
      <dl class="status-details"><div><dt>Tracking ID</dt><dd class="mono">{{ statusResult.tracking_id }}</dd></div><div><dt>Reported on</dt><dd>{{ formattedDate }}</dd></div></dl>
      <h4>Your description</h4><p class="report-description">{{ statusResult.description }}</p>
      <p class="small-note">{{ statusResult.status === 'resolved' ? 'Staff have marked this report as resolved.' : 'Check back here for updates from staff.' }}</p>
    </div>
    <div v-else-if="!error && !isLoading" class="tracking-empty"><AppIcon name="search" /><p>Your report’s progress will appear here.</p><span>No need to submit the same concern again.</span></div>
  </div>
</template>
<script setup>
import { computed, ref, watch } from 'vue'
import axios from 'axios'
import AppIcon from './AppIcon.vue'
import { API_BASE, apiError } from '../utils/api'
const props = defineProps({ initialId: { type: String, default: '' } })
const trackingId = ref(props.initialId)
const statusResult = ref(null)
const error = ref('')
const isLoading = ref(false)
watch(() => props.initialId, id => { trackingId.value = id; statusResult.value = null; error.value = '' })
const formattedDate = computed(() => statusResult.value?.created_at ? new Date(statusResult.value.created_at).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }) : 'Not available')
async function loadStatus() {
  if (isLoading.value) return
  error.value = ''
  statusResult.value = null
  const id = trackingId.value.trim().toLowerCase()
  if (!/^[a-f0-9]{8}$/.test(id)) {
    error.value = 'Enter the 8-character ID provided when you submitted your report.'
    return
  }
  isLoading.value = true
  try {
    const response = await axios.get(`${API_BASE}/status/${encodeURIComponent(id)}`, { timeout: 15000 })
    if (response.data.error) error.value = 'We couldn’t find that report. Please double-check your tracking ID.'
    else statusResult.value = response.data
  } catch (err) {
    error.value = apiError(err, 'We couldn’t check your report right now. Please try again shortly.')
  } finally {
    isLoading.value = false
  }
}
</script>
