<template>
  <div>
    <section class="hero" aria-labelledby="welcome-heading">
      <div class="hero-copy">
        <p class="eyebrow"><span class="small-rule"></span> HERE TO SUPPORT YOU</p>
        <h1 id="welcome-heading">You deserve to<br /><em>feel safe.</em></h1>
        <p class="hero-description">If something has happened, you don’t have to navigate it alone. Share your concern and take the first step towards support.</p>
        <div class="hero-reassurance"><AppIcon name="lock" /><span>No student account or name required</span></div>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div>
        <div class="art-leaf leaf-one"></div><div class="art-leaf leaf-two"></div>
        <div class="art-shield"><AppIcon name="shield" /></div>
        <span class="art-caption">A little courage. A first step.</span>
      </div>
    </section>

    <div class="workspace-grid">
      <section class="panel report-panel" aria-label="Report and tracking">
        <div class="tab-bar" role="tablist" aria-label="Choose an action" @keydown="changeTabWithKeyboard">
          <button id="report-tab" role="tab" :aria-selected="activeTab === 'report'" aria-controls="report-content" :tabindex="activeTab === 'report' ? 0 : -1" :class="['tab-button', { active: activeTab === 'report' }]" @click="activeTab = 'report'"><AppIcon name="write" /> Share a concern</button>
          <button id="track-tab" role="tab" :aria-selected="activeTab === 'track'" aria-controls="track-content" :tabindex="activeTab === 'track' ? 0 : -1" :class="['tab-button', { active: activeTab === 'track' }]" @click="activeTab = 'track'"><AppIcon name="search" /> Track a report</button>
        </div>
        <div v-show="activeTab === 'report'" id="report-content" role="tabpanel" aria-labelledby="report-tab" tabindex="0"><ComplaintForm @track="trackReport" /></div>
        <div v-show="activeTab === 'track'" id="track-content" role="tabpanel" aria-labelledby="track-tab" tabindex="0"><TrackingStatus :initial-id="trackingId" /></div>
      </section>

      <aside class="guidance-column" aria-label="Support and guidance">
        <section class="support-card">
          <span class="icon-tile"><AppIcon name="heart" /></span>
          <h2>You can start small.</h2>
          <p>It’s okay if you don’t have all the details. A short, clear description of what happened is a good place to begin.</p>
          <div class="support-divider"></div>
          <h3>Helpful things to share</h3>
          <ul class="check-list">
            <li><AppIcon name="check" />What happened or what was said</li>
            <li><AppIcon name="check" />Where or when, if you remember</li>
            <li><AppIcon name="check" />How it affected you</li>
          </ul>
          <p class="small-note">Names and evidence are optional. Share only what you feel comfortable sharing.</p>
        </section>
        <section class="next-card">
          <h2>What happens next?</h2>
          <div class="next-item"><AppIcon name="write" /><p><strong>Share your experience</strong><span>We check that your description explains an incident.</span></p></div>
          <div class="next-item"><AppIcon name="shield" /><p><strong>Receive a tracking ID</strong><span>Your report is saved for staff review.</span></p></div>
          <div class="next-item"><AppIcon name="search" /><p><strong>Check back for updates</strong><span>Use your ID to follow your report.</span></p></div>
        </section>
        <p class="urgent-note"><AppIcon name="info" /><span>If you’re in immediate danger, contact campus security or local emergency services. This form is not an emergency service.</span></p>
      </aside>
    </div>
  </div>
</template>
<script setup>
import { nextTick, ref } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import ComplaintForm from '../components/ComplaintForm.vue'
import TrackingStatus from '../components/TrackingStatus.vue'
const activeTab = ref('report')
const trackingId = ref('')
function trackReport(id) {
  trackingId.value = id
  activeTab.value = 'track'
  nextTick(() => document.getElementById('tracking-id')?.focus())
}
function changeTabWithKeyboard(event) {
  if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return
  event.preventDefault()
  activeTab.value = event.key === 'Home' ? 'report' : event.key === 'End' ? 'track' : activeTab.value === 'report' ? 'track' : 'report'
  nextTick(() => document.getElementById(`${activeTab.value}-tab`)?.focus())
}
</script>
