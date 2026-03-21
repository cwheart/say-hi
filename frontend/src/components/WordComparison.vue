<template>
  <div class="word-comparison">
    <h3 class="comparison-title">Word-by-Word Comparison</h3>
    <div class="words-container">
      <div
        v-for="(word, index) in words"
        :key="index"
        :class="['word-item', `status-${word.status}`]"
      >
        <span class="word-target">
          <template v-if="word.status === 'extra'">—</template>
          <template v-else>{{ word.target }}</template>
        </span>
        <span class="word-recognized" v-if="word.status !== 'correct'">
          <template v-if="word.status === 'missing'">skipped</template>
          <template v-else-if="word.status === 'extra'">{{ word.recognized }}</template>
          <template v-else>{{ word.recognized }}</template>
        </span>
        <span class="word-status-icon">
          <template v-if="word.status === 'correct'">✓</template>
          <template v-else-if="word.status === 'incorrect'">✗</template>
          <template v-else-if="word.status === 'missing'">⊘</template>
          <template v-else>+</template>
        </span>
      </div>
    </div>
    <div class="legend">
      <span class="legend-item"><span class="dot dot-correct"></span> Correct</span>
      <span class="legend-item"><span class="dot dot-incorrect"></span> Incorrect</span>
      <span class="legend-item"><span class="dot dot-missing"></span> Missing</span>
      <span class="legend-item"><span class="dot dot-extra"></span> Extra</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WordComparison } from '../types'

defineProps<{
  words: WordComparison[]
}>()
</script>

<style scoped>
.word-comparison {
  padding: 24px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
}

.comparison-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.words-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.word-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  position: relative;
  min-width: 48px;
}

.word-target {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}

.word-recognized {
  font-size: 11px;
  font-weight: 500;
  opacity: 0.8;
  margin-top: 2px;
}

.word-status-icon {
  position: absolute;
  top: -4px;
  right: -4px;
  font-size: 10px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}

/* Status styles */
.status-correct {
  background: #f0fdf4;
  color: #16a34a;
}

.status-correct .word-status-icon {
  background: #22c55e;
  color: white;
}

.status-incorrect {
  background: #fef2f2;
  color: #dc2626;
}

.status-incorrect .word-status-icon {
  background: #ef4444;
  color: white;
}

.status-incorrect .word-recognized {
  text-decoration: line-through;
}

.status-missing {
  background: #fff7ed;
  color: #ea580c;
}

.status-missing .word-target {
  text-decoration: line-through;
}

.status-missing .word-status-icon {
  background: #f97316;
  color: white;
}

.status-extra {
  background: #f8fafc;
  color: #94a3b8;
}

.status-extra .word-status-icon {
  background: #94a3b8;
  color: white;
}

/* Legend */
.legend {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-correct { background: #22c55e; }
.dot-incorrect { background: #ef4444; }
.dot-missing { background: #f97316; }
.dot-extra { background: #94a3b8; }
</style>
