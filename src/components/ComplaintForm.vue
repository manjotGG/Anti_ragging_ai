<template>
  <div class="form-content">
    <template v-if="!reportResult">
      <p class="eyebrow">MAKE YOURSELF HEARD</p>
      <h2 class="section-title">Share what happened</h2>
      <p class="section-description">We’re here to listen. Describe the incident in your own words.</p>
      <form @submit.prevent="submitComplaint" :aria-busy="isLoading" class="complaint-form">
        <div class="field-heading"><label for="complaint-description">Your experience <span class="required-label">(required)</span></label><span class="optional-label">Text or voice</span></div>
        <textarea id="complaint-description" ref="descriptionInput" v-model="complaint" rows="8" maxlength="5000" required :readonly="isLoading" :aria-invalid="Boolean(formError)" :aria-describedby="formError ? 'description-help description-count complaint-error' : 'description-help description-count'" placeholder="For example: A senior threatened me outside the hostel yesterday. I’m worried it could happen again." @input="formError = ''"></textarea>
        <div class="field-meta"><p id="description-help">A short sentence is enough to start. Please describe an incident.</p><span id="description-count">{{ complaint.length.toLocaleString() }} / 5,000</span></div>
        <VoiceInput :disabled="isLoading" @transcript="onTranscript" @recording="isRecording = $event" />
        <p v-if="formError" id="complaint-error" class="feedback feedback-error" role="alert"><AppIcon name="info" /><span>{{ formError }}</span></p>
        <div class="submission-note"><AppIcon name="lock" /><p>You don’t need to include your name. Your description will be shared with staff who review reports.</p></div>
        <div class="form-actions"><span class="small-note">One step at a time.</span><button type="submit" class="primary-button" :disabled="isLoading || isRecording || !complaint.trim()"><span v-if="isLoading" class="spinner" aria-hidden="true"></span><AppIcon v-else name="shield" />{{ isLoading ? 'Checking your report…' : 'Submit report' }}</button></div>
        <p v-if="isLoading" role="status" class="small-note">This may take a moment. Please keep this page open.</p>
      </form>
    </template>
    <div v-else class="success-content" role="status" aria-live="polite">
      <span class="success-icon"><AppIcon name="check" /></span>
      <p class="eyebrow">YOUR REPORT IS SAVED</p>
      <h2 class="section-title">Thank you for speaking up.</h2>
      <p class="section-description">{{ reportResult.support_message }}</p>
      <div class="tracking-receipt"><label for="receipt-id">Your tracking ID</label><div class="receipt-row"><input id="receipt-id" :value="reportResult.tracking_id" readonly /><button type="button" class="secondary-button" @click="copyId"><AppIcon name="copy" />{{ copyMessage || 'Copy ID' }}</button></div><p>Keep this ID somewhere private. You’ll need it to check updates.</p></div>
      <p class="small-note">Your report is awaiting staff review.</p>
      <div class="success-actions"><button class="primary-button" @click="emit('track', reportResult.tracking_id)">Track this report</button><button class="secondary-button" @click="startNewReport">Share another concern</button></div>
    </div>
  </div>
</template>
<script setup>
import { nextTick, ref } from 'vue'
import axios from 'axios'
import VoiceInput from './VoiceInput.vue'
import AppIcon from './AppIcon.vue'
import { API_BASE, apiError } from '../utils/api'
import { descriptionError } from '../utils/validation'
const emit = defineEmits(['track'])
const complaint = ref('')
const reportResult = ref(null)
const isLoading = ref(false)
const isRecording = ref(false)
const formError = ref('')
const copyMessage = ref('')
const descriptionInput = ref(null)
function onTranscript(text) {
  // Voice is inserted without overwriting text the student has already written.
  complaint.value = [complaint.value.trim(), text.trim()].filter(Boolean).join(' ').slice(0, 5000)
  formError.value = ''
}
async function copyId() {
  try {
    await navigator.clipboard.writeText(reportResult.value.tracking_id)
    copyMessage.value = 'Copied'
  } catch {
    copyMessage.value = 'Select ID to copy'
  }
}
async function startNewReport() {
  reportResult.value = null
  copyMessage.value = ''
  await nextTick()
  descriptionInput.value?.focus()
}
async function submitComplaint() {
  if (isLoading.value || isRecording.value) return
  const payload = complaint.value.normalize('NFC').trim()
  formError.value = descriptionError(payload)
  if (formError.value) {
    descriptionInput.value?.focus()
    return
  }
  isLoading.value = true
  try {
    const response = await axios.post(`${API_BASE}/report`, { description: payload }, { timeout: 45000 })
    reportResult.value = response.data
    complaint.value = ''
  } catch (error) {
    formError.value = apiError(error, 'We couldn’t submit your report. Your text is still here. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>
