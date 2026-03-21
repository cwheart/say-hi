<template>
  <view class="history-page">
    <view class="history-list container">
      <view
        v-for="item in historyList"
        :key="item.id"
        class="history-card card"
      >
        <view class="history-header">
          <text class="history-text">{{ item.target_text }}</text>
          <text class="history-score" :style="{ color: getScoreColor(item.overall_score) }">
            {{ item.overall_score }}
          </text>
        </view>
        <text class="history-date text-muted">{{ formatDate(item.created_at) }}</text>
      </view>

      <view v-if="historyList.length === 0 && !loading" class="empty-state text-center">
        <text class="text-muted">No practice history yet</text>
      </view>

      <view v-if="loading" class="loading-state text-center">
        <text class="text-muted">加载中...</text>
      </view>

      <view v-if="!loading && !noMore && historyList.length > 0" class="load-more text-center">
        <text class="text-muted">上拉加载更多</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onShow, onReachBottom } from '@dcloudio/uni-app'
import { get } from '@/utils/request'
import { ensureLogin } from '@/utils/auth'
import type { HistoryItem, PaginatedResponse } from '@/types'

const historyList = ref<HistoryItem[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const noMore = ref(false)

function getScoreColor(score: number): string {
  if (score >= 80) return '#22c55e'
  if (score >= 60) return '#f59e0b'
  return '#ef4444'
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${day} ${h}:${min}`
}

async function loadHistory(reset = false) {
  if (loading.value) return
  if (!reset && noMore.value) return

  if (reset) {
    page.value = 1
    noMore.value = false
    historyList.value = []
  }

  loading.value = true
  try {
    const response = await get<PaginatedResponse<HistoryItem>>(
      `/wx/history?page=${page.value}&page_size=${pageSize}`
    )
    // Extract items from the paginated response
    const items = response.items || []
    if (items.length < pageSize) {
      noMore.value = true
    }
    historyList.value = [...historyList.value, ...items]
    page.value++
  } catch (e) {
    console.error('Failed to load history:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

onShow(async () => {
  try {
    await ensureLogin()
    await loadHistory(true)
  } catch {
    // redirect handled by ensureLogin
  }
})

onReachBottom(() => {
  loadHistory()
})
</script>

<style scoped>
.history-page {
  padding-bottom: 30rpx;
}

.history-card {
  padding: 30rpx;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-text {
  font-size: 30rpx;
  font-weight: 500;
  color: #1e293b;
  flex: 1;
  margin-right: 16rpx;
}

.history-score {
  font-size: 36rpx;
  font-weight: 700;
  flex-shrink: 0;
}

.history-date {
  font-size: 24rpx;
  margin-top: 10rpx;
  display: block;
}

.empty-state,
.loading-state,
.load-more {
  padding: 60rpx 0;
}
</style>