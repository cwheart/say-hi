<template>
  <view class="score-card">
    <view class="score-header">
      <text class="score-label">{{ label }}</text>
      <text class="score-value" :style="{ color: scoreColor }">{{ score }}</text>
    </view>
    <view class="progress-bar">
      <view
        class="progress-fill"
        :style="{ width: score + '%', backgroundColor: scoreColor }"
      />
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  label: string
  score: number
}>()

const scoreColor = computed(() => {
  if (props.score >= 80) return '#22c55e'
  if (props.score >= 60) return '#f59e0b'
  return '#ef4444'
})
</script>

<style scoped>
.score-card {
  margin-bottom: 24rpx;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.score-label {
  font-size: 28rpx;
  color: #475569;
}

.score-value {
  font-size: 32rpx;
  font-weight: 600;
}

.progress-bar {
  height: 16rpx;
  background-color: #e2e8f0;
  border-radius: 8rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 8rpx;
  transition: width 0.5s ease;
}
</style>