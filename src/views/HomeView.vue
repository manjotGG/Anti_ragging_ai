<template>
  <div class="space-y-8">
    <section class="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-soft transition duration-300 dark:border-slate-700/80 dark:bg-slate-900/95">
      <ComplaintForm />
    </section>
    <section class="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-soft transition duration-300 dark:border-slate-700/80 dark:bg-slate-900/95">
      <TrackingStatus />
    </section>
  </div>
</template>

<script setup>
import ComplaintForm from '../components/ComplaintForm.vue'
import TrackingStatus from '../components/TrackingStatus.vue'
</script>
