<template>
  <view class="result-page container">
    <view v-if="result">
      <!-- Overall Score -->
      <view class="overall-card card text-center">
        <text class="overall-label">综合评分</text>
        <text class="overall-score" :style="{ color: overallColor }">{{ result.scores.overall }}</text>
      </view>

      <!-- Detail Scores -->
      <view class="card">
        <score-card label="准确度 Accuracy" :score="result.scores.accuracy" />
        <score-card label="完整度 Completeness" :score="result.scores.completeness" />
        <score-card label="流利度 Fluency" :score="result.scores.fluency" />
      </view>

      <!-- Word Comparison -->
      <view v-if="result.word_comparison?.length" class="card">
        <text class="section-title">逐词对比</text>
        <word-compare :words="result.word_comparison" />
        <view class="legend">
          <text class="legend-item word-correct">✓ 正确</text>
          <text class="legend-item word-incorrect">✗ 错误</text>
          <text class="legend-item word-missing">? 缺失</text>
          <text class="legend-item word-extra">+ 多余</text>
        </view>
      </view>

      <!-- Actions -->
      <view class="actions">
        <view class="btn-primary" @tap="handleTryAgain">
          <text>再试一次</text>
        </view>
      </view>
    </view>

    <view v-else class="empty-state text-center">
      <text class="text-muted">暂无评分数据</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import ScoreCard from '@/components/score-card.vue'
import WordCompare from '@/components/word-compare.vue'
import type { EvaluationResult } from '@/types'

const result = ref<EvaluationResult | null>(null)

const overallColor = computed(() => {
  if (!result.value) return '#94a3b8'
  const s = result.value.scores.overall
  if (s >= 80) return '#22c55e'
  if (s >= 60) return '#f59e0b'
  return '#ef4444'
})

function handleTryAgain() {
  uni.navigateBack()
}

onLoad((query) => {
  if (query?.data) {
    try {
      result.value = JSON.parse(decodeURIComponent(query.data))
    } catch (e) {
      console.error('Failed to parse result data:', e)
    }
  }
})
</script>

<style scoped>
.overall-card {
  padding: 40rpx;
}

.overall-label {
  font-size: 28rpx;
  color: #94a3b8;
  display: block;
  margin-bottom: 12rpx;
}

.overall-score {
  font-size: 96rpx;
  font-weight: 700;
  display: block;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #1e293b;
  display: block;
  margin-bottom: 16rpx;
}

.legend {
  display: flex;
  gap: 20rpx;
  margin-top: 16rpx;
  flex-wrap: wrap;
}

.legend-item {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
}

.word-correct { color: #166534; background-color: #dcfce7; }
.word-incorrect { color: #991b1b; background-color: #fee2e2; }
.word-missing { color: #9a3412; background-color: #ffedd5; }
.word-extra { color: #6b7280; background-color: #f3f4f6; }

.actions {
  margin-top: 40rpx;
}

.empty-state {
  padding: 100rpx 0;
}
</style>