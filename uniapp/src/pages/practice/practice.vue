<template>
  <view class="practice-page container">
    <!-- Loading -->
    <view v-if="loading" class="loading-state text-center">
      <text class="text-muted">加载中...</text>
    </view>

    <!-- Practice Detail -->
    <view v-else-if="practice">
      <view class="card">
        <view class="practice-meta-row">
          <view class="badge" :class="'badge-' + practice.difficulty">
            <text>{{ practice.difficulty }}</text>
          </view>
          <text class="category-tag">{{ practice.category }}</text>
        </view>
        <view class="target-text-row">
          <text class="target-text">{{ practice.text }}</text>
          <view
            v-if="practice.audio_url"
            class="speaker-btn"
            :class="{ playing: audioPlaying }"
            @tap="handlePlayAudio"
          >
            <text class="speaker-icon">🔊</text>
          </view>
        </view>
        <text v-if="practice.hint" class="hint-text">💡 {{ practice.hint }}</text>
        <text v-if="bestScore >= 0" class="best-score">🏆 最佳: {{ bestScore }}分</text>
      </view>

      <!-- Recorder -->
      <view class="recorder-section">
        <view class="record-timer" v-if="recordState === 'recording'">
          <text class="timer-text">{{ formatTime(recordingTime) }}</text>
          <view class="pulse-dot" />
        </view>

        <view class="record-btn-wrap">
          <view
            v-if="recordState === 'idle'"
            class="record-btn"
            @tap="handleStart"
          >
            <text class="record-btn-icon">🎤</text>
            <text class="record-btn-label">点击录音</text>
          </view>

          <view
            v-else-if="recordState === 'recording'"
            class="record-btn recording"
            @tap="handleStop"
          >
            <text class="record-btn-icon">⏹</text>
            <text class="record-btn-label">停止</text>
          </view>

          <view v-else-if="recordState === 'recorded'" class="recorded-actions">
            <view class="btn-secondary" @tap="handleReset">
              <text>重录</text>
            </view>
            <view class="btn-primary submit-btn" :class="{ disabled: submitting }" @tap="handleSubmit">
              <text>{{ submitting ? '评分中...' : '提交评分' }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- Not Found -->
    <view v-else class="empty-state text-center">
      <text class="text-muted">练习未找到</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { get } from '@/utils/request'
import { uploadFile } from '@/utils/upload'
import { startRecording, stopRecording, isRecordingSupported } from '@/utils/recorder'
import { playAudio, stopAudio, isAudioPlaying, destroyAudioPlayer } from '@/utils/audio-player'
import type { RecordingResult } from '@/utils/recorder'
import type { Practice, EvaluationResult } from '@/types'

const practice = ref<Practice | null>(null)
const loading = ref(true)
const bestScore = ref(-1)
const recordState = ref<'idle' | 'recording' | 'recorded'>('idle')
const recordingTime = ref(0)
const submitting = ref(false)
const audioPlaying = ref(false)

let recordResult: RecordingResult | null = null
let timer: ReturnType<typeof setInterval> | null = null

function formatTime(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function handleStart() {
  if (!isRecordingSupported()) {
    uni.showToast({ title: '请使用现代浏览器或微信小程序进行录音', icon: 'none' })
    return
  }

  recordingTime.value = 0
  startRecording({
    onStart: () => {
      recordState.value = 'recording'
      timer = setInterval(() => {
        recordingTime.value += 1000
      }, 1000)
    },
    onStop: (result) => {
      if (timer) {
        clearInterval(timer)
        timer = null
      }
      recordResult = result
      recordState.value = 'recorded'
    },
    onError: (err) => {
      if (timer) {
        clearInterval(timer)
        timer = null
      }
      recordState.value = 'idle'
      uni.showToast({ title: err, icon: 'none' })
    },
  })
}

function handleStop() {
  stopRecording()
}

function handleReset() {
  recordState.value = 'idle'
  recordResult = null
  recordingTime.value = 0
}

async function handleSubmit() {
  if (!recordResult || !practice.value || submitting.value) return

  submitting.value = true
  try {
    const formData: Record<string, string> = {
      target_text: practice.value.text,
      practice_id: practice.value.id,
    }

    const result = await uploadFile({
      url: '/wx/evaluate',
      filePath: recordResult.tempFilePath || undefined,
      fileBlob: recordResult.blob || undefined,
      fileName: 'recording.webm',
      formData,
    }) as EvaluationResult

    // Navigate to result page with data
    const encoded = encodeURIComponent(JSON.stringify(result))
    uni.navigateTo({ url: `/pages/result/result?data=${encoded}` })
  } catch (e: any) {
    uni.showToast({ title: e?.message || '提交失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}

onLoad(async (query) => {
  const id = query?.id
  if (!id) {
    loading.value = false
    return
  }

  try {
    practice.value = await get<Practice>(`/wx/practices/${id}`)
    // Try to get best score
    try {
      const response = await get<PaginatedResponse<any>>(`/wx/history?practice_id=${id}&page_size=1`)
      if (response.items && response.items.length > 0) {
        bestScore.value = response.items[0].overall_score
      }
    } catch {
      // Best score is optional
    }
  } catch (e) {
    console.error('Failed to load practice:', e)
  } finally {
    loading.value = false
  }
})

function handlePlayAudio() {
  if (!practice.value?.audio_url) return

  if (isAudioPlaying()) {
    stopAudio()
    audioPlaying.value = false
    return
  }

  const url = practice.value.audio_url
  playAudio(url, {
    onPlay: () => {
      audioPlaying.value = true
    },
    onStop: () => {
      audioPlaying.value = false
    },
    onError: () => {
      audioPlaying.value = false
      uni.showToast({ title: '播放失败', icon: 'none' })
    },
  })
}

onUnmounted(() => {
  if (timer) clearInterval(timer)
  destroyAudioPlayer()
})
</script>

<style scoped>
.practice-meta-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.badge {
  padding: 6rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
}

.badge-easy { background-color: #dcfce7; color: #166534; }
.badge-medium { background-color: #fef9c3; color: #854d0e; }
.badge-hard { background-color: #fee2e2; color: #991b1b; }

.category-tag {
  font-size: 24rpx;
  color: #3b82f6;
  background-color: #eff6ff;
  padding: 4rpx 14rpx;
  border-radius: 6rpx;
}

.target-text-row {
  display: flex;
  align-items: flex-start;
  gap: 16rpx;
}

.target-text {
  font-size: 40rpx;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
  margin-bottom: 16rpx;
  line-height: 1.5;
}

.speaker-btn {
  flex-shrink: 0;
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background-color: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 8rpx;
}

.speaker-btn.playing {
  background-color: #3b82f6;
  animation: speaker-pulse 0.8s ease-in-out infinite;
}

.speaker-icon {
  font-size: 36rpx;
}

@keyframes speaker-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
}

.hint-text {
  font-size: 26rpx;
  color: #94a3b8;
  display: block;
  margin-bottom: 8rpx;
}

.best-score {
  font-size: 26rpx;
  color: #f59e0b;
  display: block;
}

/* Recorder Section */
.recorder-section {
  margin-top: 40rpx;
  text-align: center;
}

.record-timer {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30rpx;
  gap: 12rpx;
}

.timer-text {
  font-size: 48rpx;
  font-weight: 600;
  color: #ef4444;
  font-variant-numeric: tabular-nums;
}

.pulse-dot {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background-color: #ef4444;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.record-btn-wrap {
  display: flex;
  justify-content: center;
}

.record-btn {
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;
  background-color: #3b82f6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.record-btn.recording {
  background-color: #ef4444;
}

.record-btn-icon {
  font-size: 56rpx;
}

.record-btn-label {
  font-size: 24rpx;
  color: #ffffff;
  margin-top: 8rpx;
}

.recorded-actions {
  display: flex;
  gap: 24rpx;
  justify-content: center;
}

.btn-secondary {
  background-color: #f1f5f9;
  color: #475569;
  border-radius: 16rpx;
  padding: 24rpx 48rpx;
  font-size: 32rpx;
}

.submit-btn {
  padding: 24rpx 48rpx;
}

.disabled {
  opacity: 0.6;
}

.loading-state,
.empty-state {
  padding: 100rpx 0;
}
</style>