<template>
  <div class="audio-recorder">
    <!-- Error display -->
    <div v-if="error" class="recorder-error">
      <span class="error-icon">⚠️</span>
      <span>{{ error }}</span>
    </div>

    <!-- Timer display -->
    <div class="recorder-timer" :class="{ recording: state === 'recording' }">
      <span class="timer-dot" v-if="state === 'recording'"></span>
      <span class="timer-text">{{ formatDuration(duration) }}</span>
      <span class="timer-max" v-if="state === 'recording'">/ {{ formatDuration(maxDuration) }}</span>
    </div>

    <!-- Progress bar -->
    <div class="recorder-progress" v-if="state === 'recording'">
      <div class="progress-bar" :style="{ width: `${(duration / maxDuration) * 100}%` }"></div>
    </div>

    <!-- Controls -->
    <div class="recorder-controls">
      <!-- Idle: show record button -->
      <button
        v-if="state === 'idle'"
        class="btn btn-record"
        @click="startRecording"
        :disabled="!isSupported"
      >
        <span class="btn-icon">🎤</span>
        <span>Record</span>
      </button>

      <!-- Recording: show stop button -->
      <button
        v-if="state === 'recording'"
        class="btn btn-stop"
        @click="stopRecording"
      >
        <span class="btn-icon">⏹</span>
        <span>Stop</span>
      </button>

      <!-- Recorded: show play, re-record -->
      <template v-if="state === 'recorded'">
        <button class="btn btn-play" @click="playRecording">
          <span class="btn-icon">▶️</span>
          <span>Play</span>
        </button>
        <button class="btn btn-rerecord" @click="resetRecording">
          <span class="btn-icon">🔄</span>
          <span>Re-record</span>
        </button>
      </template>

      <!-- Playing: show stop button -->
      <template v-if="state === 'playing'">
        <button class="btn btn-stop" @click="stopPlaying">
          <span class="btn-icon">⏹</span>
          <span>Stop</span>
        </button>
        <button class="btn btn-rerecord" @click="resetRecording">
          <span class="btn-icon">🔄</span>
          <span>Re-record</span>
        </button>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAudioRecorder } from '../composables/useAudioRecorder'

const {
  state,
  audioBlob,
  duration,
  error,
  isSupported,
  maxDuration,
  startRecording,
  stopRecording,
  playRecording,
  stopPlaying,
  resetRecording,
  formatDuration,
} = useAudioRecorder()

defineExpose({
  audioBlob,
  state,
  resetRecording,
})
</script>

<style scoped>
.audio-recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
}

.recorder-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
  width: 100%;
}

.error-icon {
  flex-shrink: 0;
}

.recorder-timer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 32px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #334155;
}

.recorder-timer.recording {
  color: #ef4444;
}

.timer-dot {
  width: 12px;
  height: 12px;
  background: #ef4444;
  border-radius: 50%;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.timer-max {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 400;
}

.recorder-progress {
  width: 100%;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #ef4444;
  border-radius: 2px;
  transition: width 1s linear;
}

.recorder-controls {
  display: flex;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 18px;
}

.btn-record {
  background: #ef4444;
  color: white;
}

.btn-record:hover:not(:disabled) {
  background: #dc2626;
  transform: scale(1.05);
}

.btn-stop {
  background: #64748b;
  color: white;
}

.btn-stop:hover {
  background: #475569;
}

.btn-play {
  background: #22c55e;
  color: white;
}

.btn-play:hover {
  background: #16a34a;
}

.btn-rerecord {
  background: #f1f5f9;
  color: #475569;
}

.btn-rerecord:hover {
  background: #e2e8f0;
}
</style>
