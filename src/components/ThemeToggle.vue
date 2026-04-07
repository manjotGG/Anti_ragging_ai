<template>
  <button @click="toggleTheme" class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-800 shadow-sm transition duration-300 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700">
    <span v-if="isDark">☀️ Light</span>
    <span v-else>🌙 Dark</span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'theme'
const isDark = ref(false)

function applyTheme(value) {
  isDark.value = value === 'dark'
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem(STORAGE_KEY, value)
}

function toggleTheme() {
  applyTheme(isDark.value ? 'light' : 'dark')
}

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY) || 'dark'
  applyTheme(saved)
})
</script>
