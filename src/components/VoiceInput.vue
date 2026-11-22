<template>
  <div class="voice-input">
    <div class="voice-row"><button type="button" class="voice-button" :disabled="disabled || !isSupported" :aria-pressed="isRecording" @click="toggleRecording"><AppIcon name="mic" />{{ isRecording ? 'Stop dictation' : 'Use voice instead' }}</button><span v-if="isRecording" class="recording-label" role="status">Listening…</span><span v-else class="small-note">{{ isSupported ? 'Review your words before submitting.' : 'Voice input isn’t supported here. You can type above.' }}</span></div>
    <p v-if="interimTranscript" class="voice-transcript" role="status">{{ interimTranscript }}</p>
    <p v-if="errorMessage" role="alert" class="feedback feedback-error">{{ errorMessage }}</p>
  </div>
</template>
<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import AppIcon from './AppIcon.vue'
defineProps({ disabled: { type: Boolean, default: false } })
const emit = defineEmits(['transcript', 'recording'])
const interimTranscript = ref('')
const isRecording = ref(false)
const errorMessage = ref('')
const isSupported = Boolean(window.SpeechRecognition || window.webkitSpeechRecognition)
let recognition = null
function setRecording(value) { isRecording.value = value; emit('recording', value) }
onMounted(() => {
  const Recognizer = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!Recognizer) return
  recognition = new Recognizer()
  recognition.continuous = true
  recognition.interimResults = true
  recognition.lang = 'en-IN'
  recognition.onresult = event => {
    let interim = ''
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      if (event.results[i].isFinal) emit('transcript', event.results[i][0].transcript)
      else interim += event.results[i][0].transcript
    }
    interimTranscript.value = interim
  }
  recognition.onerror = event => {
    errorMessage.value = event.error === 'not-allowed' ? 'Microphone access wasn’t allowed. You can still type your report.' : 'Dictation stopped. You can try again or continue typing.'
    setRecording(false)
  }
  recognition.onend = () => { setRecording(false); interimTranscript.value = '' }
})
function toggleRecording() {
  if (isRecording.value) { recognition?.stop(); return }
  if (!recognition) return
  errorMessage.value = ''
  try { recognition.start(); setRecording(true) }
  catch { errorMessage.value = 'Couldn’t start dictation. Please try again or type your report.'; setRecording(false) }
}
onUnmounted(() => {
  if (!recognition) return
  recognition.onresult = recognition.onerror = recognition.onend = null
  recognition.abort()
})
</script>
