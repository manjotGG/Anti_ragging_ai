<template>
  <button @click="toggleTheme" class="theme-button" :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'" :title="isDark ? 'Switch to light theme' : 'Switch to dark theme'"><AppIcon :name="isDark ? 'sun' : 'moon'" /></button>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import AppIcon from './AppIcon.vue'
const isDark = ref(document.documentElement.classList.contains('dark'))
function applyTheme(value) {
  isDark.value = value === 'dark'
  document.documentElement.classList.toggle('dark', isDark.value)
}
function toggleTheme() {
  const value = isDark.value ? 'light' : 'dark'
  applyTheme(value)
  try { localStorage.setItem('theme', value) } catch { /* Theme still works without storage. */ }
}
onMounted(() => {
  let saved
  try { saved = localStorage.getItem('theme') } catch { /* Use light by default. */ }
  applyTheme(saved || 'light')
})
</script>
