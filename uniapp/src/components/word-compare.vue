<template>
  <view class="word-compare">
    <text
      v-for="(item, index) in words"
      :key="index"
      class="word-item"
      :class="'word-' + item.status"
    >{{ item.word }}</text>
  </view>
</template>

<script setup lang="ts">
import type { WordComparison } from '@/types'

defineProps<{
  words: WordComparison[]
}>()
</script>

<style scoped>
.word-compare {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  padding: 20rpx 0;
}

.word-item {
  font-size: 32rpx;
  padding: 6rpx 12rpx;
  border-radius: 8rpx;
  font-weight: 500;
}

.word-correct {
  color: #166534;
  background-color: #dcfce7;
}

.word-incorrect {
  color: #991b1b;
  background-color: #fee2e2;
  text-decoration: line-through;
}

.word-missing {
  color: #9a3412;
  background-color: #ffedd5;
  font-style: italic;
}

.word-extra {
  color: #6b7280;
  background-color: #f3f4f6;
  text-decoration: line-through;
}
</style>