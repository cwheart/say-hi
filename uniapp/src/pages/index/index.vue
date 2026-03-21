<template>
  <view class="index-page">
    <!-- Category Tabs -->
    <scroll-view scroll-x class="tab-bar">
      <view
        v-for="tab in tabs"
        :key="tab.value"
        class="tab-item"
        :class="{ active: currentTab === tab.value }"
        @tap="currentTab = tab.value"
      >
        <text>{{ tab.label }}</text>
      </view>
    </scroll-view>

    <!-- Practice List -->
    <view class="practice-list">
      <view
        v-for="item in filteredList"
        :key="item.id"
        class="practice-card card"
        @tap="goToPractice(item.id)"
      >
        <view class="practice-header">
          <text class="practice-text">{{ item.text }}</text>
          <view class="badge" :class="'badge-' + item.difficulty">
            <text>{{ item.difficulty }}</text>
          </view>
        </view>
        <view class="practice-meta">
          <text class="category-tag">{{ item.category }}</text>
          <text v-if="item.hint" class="hint-text">💡 {{ item.hint }}</text>
        </view>
      </view>

      <view v-if="filteredList.length === 0 && !loading" class="empty-state">
        <text class="text-muted">暂无练习题目</text>
      </view>

      <view v-if="loading" class="loading-state">
        <text class="text-muted">加载中...</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { get } from '@/utils/request'
import { ensureLogin } from '@/utils/auth'
import type { Practice, PracticeListResponse } from '@/types'

const tabs = [
  { label: '全部', value: 'all' },
  { label: 'Word', value: 'word' },
  { label: 'Phrase', value: 'phrase' },
  { label: 'Sentence', value: 'sentence' },
]

const currentTab = ref('all')
const practiceList = ref<Practice[]>([])
const loading = ref(false)

const filteredList = computed(() => {
  if (currentTab.value === 'all') return practiceList.value
  return practiceList.value.filter((p) => p.category === currentTab.value)
})

async function loadPractices() {
  loading.value = true
  try {
    const response = await get<PracticeListResponse>('/wx/practices')
    // Extract items from the response object
    practiceList.value = response.items || []
  } catch (e) {
    console.error('Failed to load practices:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

function goToPractice(id: string) {
  uni.navigateTo({ url: `/pages/practice/practice?id=${id}` })
}

onShow(async () => {
  try {
    await ensureLogin()
    await loadPractices()
  } catch (e) {
    // ensureLogin may redirect to login on H5
  }
})
</script>

<style scoped>
.index-page {
  padding-bottom: 30rpx;
}

.tab-bar {
  display: flex;
  white-space: nowrap;
  padding: 20rpx 30rpx;
  background-color: #ffffff;
}

.tab-item {
  display: inline-block;
  padding: 14rpx 32rpx;
  margin-right: 16rpx;
  border-radius: 32rpx;
  font-size: 28rpx;
  color: #64748b;
  background-color: #f1f5f9;
}

.tab-item.active {
  color: #ffffff;
  background-color: #3b82f6;
}

.practice-list {
  padding: 20rpx 30rpx;
}

.practice-card {
  padding: 30rpx;
}

.practice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.practice-text {
  font-size: 32rpx;
  font-weight: 500;
  color: #1e293b;
  flex: 1;
  margin-right: 16rpx;
}

.badge {
  padding: 6rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  flex-shrink: 0;
}

.badge-easy {
  background-color: #dcfce7;
  color: #166534;
}

.badge-medium {
  background-color: #fef9c3;
  color: #854d0e;
}

.badge-hard {
  background-color: #fee2e2;
  color: #991b1b;
}

.practice-meta {
  display: flex;
  align-items: center;
  margin-top: 16rpx;
  gap: 16rpx;
}

.category-tag {
  font-size: 24rpx;
  color: #3b82f6;
  background-color: #eff6ff;
  padding: 4rpx 14rpx;
  border-radius: 6rpx;
}

.hint-text {
  font-size: 24rpx;
  color: #94a3b8;
}

.empty-state,
.loading-state {
  text-align: center;
  padding: 80rpx 0;
}
</style>