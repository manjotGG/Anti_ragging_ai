<template>
  <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-950">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-sm font-medium text-slate-700 dark:text-slate-200">Voice input</p>
        <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">Use your microphone to dictate the complaint.</p>
      </div>
      <button @click="toggleRecording" class="inline-flex items-center gap-2 rounded-full bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500">
        <span v-if="isRecording">Stop</span>
        <span v-else>Record</span>
      </button>
    </div>

    <div class="mt-4 rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300">
      <p class="font-semibold">Live transcription</p>
      <p class="mt-2 min-h-[4rem] whitespace-pre-line">{{ transcript || 'Press record to start transcribing.' }}</p>
    </div>

    <p v-if="errorMessage" class="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-700/40 dark:bg-red-950/40 dark:text-red-200">{{ errorMessage }}</p>
    <p v-else class="mt-4 text-sm text-slate-500 dark:text-slate-400">{{ isSupported ? 'Speech recognition ready.' : 'SpeechRecognition API not supported in this browser.' }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['transcript'])
const transcript = ref('')
const isRecording = ref(false)
const errorMessage = ref('')
const isSupported = Boolean(window.SpeechRecognition || window.webkitSpeechRecognition)
let recognition = null

function setupRecognition() {
  const Recognizer = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!Recognizer) return

  recognition = new Recognizer()
  recognition.continuous = true
  recognition.interimResults = true
  recognition.lang = 'en-US'

  recognition.onresult = (event) => {
    let latest = ''
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      latest += event.results[i][0].transcript
    }
    transcript.value = latest.trim()
    emit('transcript', transcript.value)
  }

  recognition.onerror = (event) => {
    errorMessage.value = `Speech recognition error: ${event.error}`
    stopRecording()
  }

  recognition.onend = () => {
    isRecording.value = false
  }
}

function startRecording() {
  if (!recognition) {
    errorMessage.value = 'SpeechRecognition not available.'
    return
  }
  errorMessage.value = ''
  transcript.value = ''
  recognition.start()
  isRecording.value = true
}

function stopRecording() {
  if (recognition) {
    recognition.stop()
  }
  isRecording.value = false
}

function toggleRecording() {
  if (!isSupported) {
    errorMessage.value = 'Your browser does not support voice input.'
    return
  }
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

onMounted(() => {
  setupRecognition()
})

onUnmounted(() => {
  stopRecording()
})
</script>
