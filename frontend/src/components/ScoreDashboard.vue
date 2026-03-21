<template>
  <div class="score-dashboard">
    <!-- Overall score -->
    <div class="overall-score">
      <div class="score-circle" :style="{ borderColor: overallColor }">
        <span class="score-number" :style="{ color: overallColor }">{{ scores.overall }}</span>
        <span class="score-label">Overall</span>
      </div>
      <div class="score-level" :style="{ color: overallColor }">{{ level }}</div>
    </div>

    <!-- Dimension scores -->
    <div class="dimension-scores">
      <div class="dimension" v-for="dim in dimensions" :key="dim.key">
        <div class="dimension-header">
          <span class="dimension-icon">{{ dim.icon }}</span>
          <span class="dimension-name">{{ dim.label }}</span>
        </div>
        <div class="dimension-bar-container">
          <div
            class="dimension-bar"
            :style="{ width: `${dim.value}%`, background: getScoreColor(dim.value) }"
          ></div>
        </div>
        <span class="dimension-value" :style="{ color: getScoreColor(dim.value) }">{{ dim.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Scores } from '../types'
import { getScoreLevel, getScoreColor } from '../types'

const props = defineProps<{
  scores: Scores
}>()

const overallColor = computed(() => getScoreColor(props.scores.overall))
const level = computed(() => getScoreLevel(props.scores.overall))

const dimensions = computed(() => [
  { key: 'accuracy', label: 'Accuracy', icon: '🎯', value: props.scores.accuracy },
  { key: 'completeness', label: 'Completeness', icon: '📋', value: props.scores.completeness },
  { key: 'fluency', label: 'Fluency', icon: '🌊', value: props.scores.fluency },
])
</script>

<style scoped>
.score-dashboard {
  padding: 24px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
}

.overall-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 6px solid;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.score-number {
  font-size: 42px;
  font-weight: 800;
  line-height: 1;
}

.score-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
}

.score-level {
  font-size: 24px;
  font-weight: 800;
}

.dimension-scores {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dimension {
  display: grid;
  grid-template-columns: 140px 1fr 40px;
  align-items: center;
  gap: 12px;
}

.dimension-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dimension-icon {
  font-size: 16px;
}

.dimension-name {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.dimension-bar-container {
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.dimension-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s ease-out;
}

.dimension-value {
  font-size: 16px;
  font-weight: 700;
  text-align: right;
}

@media (max-width: 480px) {
  .dimension {
    grid-template-columns: 120px 1fr 36px;
  }
}
</style>
