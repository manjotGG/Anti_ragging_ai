<template>
  <div class="app-shell">
    <a href="#main-content" class="skip-link">Skip to content</a>
    <header class="site-header">
      <div class="header-inner">
        <router-link to="/" class="brand" aria-label="Student Care home">
          <span class="brand-mark"><AppIcon name="shield" /></span>
          <span>Student<span class="brand-light">Care</span><span class="brand-caption">ANTI-RAGGING SUPPORT</span></span>
        </router-link>
        <div class="header-actions">
          <span class="header-note">Your voice matters.</span>
          <ThemeToggle />
          <router-link v-if="auth.state.token" to="/admin/dashboard" class="quiet-link">Dashboard</router-link>
          <button v-if="auth.state.token" @click="handleLogout" class="quiet-link">Sign out</button>
          <router-link v-else to="/admin/login" class="quiet-link">Staff sign in</router-link>
        </div>
      </div>
    </header>
    <main id="main-content" class="main-container" tabindex="-1"><router-view /></main>
    <footer class="site-footer">
      <span class="footer-brand"><AppIcon name="shield" /> StudentCare</span>
      <p>Every student deserves respect. Every concern deserves to be heard.</p>
      <span>Take it at your pace.</span>
    </footer>
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'
import AppIcon from './components/AppIcon.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import auth from './store/auth'
const router = useRouter()
function handleLogout() {
  auth.logout()
  router.push({ name: 'Home' })
}
</script>
