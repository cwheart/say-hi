<template>
  <div v-if="!isSupported" class="browser-warning">
    <span class="warning-icon">⚠️</span>
    <div class="warning-content">
      <strong>Browser Not Supported</strong>
      <p>
        Your browser does not support audio recording (MediaRecorder API).
        Please use a modern browser like
        <strong>Chrome</strong>, <strong>Firefox</strong>, or <strong>Edge</strong>.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isSupported = ref(
  typeof window !== 'undefined' &&
  typeof navigator.mediaDevices?.getUserMedia === 'function' &&
  typeof MediaRecorder !== 'undefined'
)
</script>

<style scoped>
.browser-warning {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 900px;
  margin: 16px auto;
  padding: 16px 20px;
  background: #fef3c7;
  border: 1px solid #fbbf24;
  border-radius: 12px;
  color: #92400e;
}

.warning-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.warning-content strong {
  display: block;
  margin-bottom: 4px;
}

.warning-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}
</style>
