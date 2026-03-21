<template>
  <div class="evaluation-result">
    <h2 class="result-title">📊 Your Results</h2>

    <div class="result-recognized">
      <label class="section-label">What we heard:</label>
      <p class="recognized-text">
        {{ result.recognized_text || '(No speech detected)' }}
      </p>
    </div>

    <ScoreDashboard :scores="result.scores" />

    <WordComparisonComponent :words="result.word_comparison" />

    <button class="btn-try-again" @click="$emit('try-again')">
      🔄 Try Again
    </button>
  </div>
</template>

<script setup lang="ts">
import type { EvaluationResult } from '../types'
import ScoreDashboard from './ScoreDashboard.vue'
import WordComparisonComponent from './WordComparison.vue'

defineProps<{
  result: EvaluationResult
}>()

defineEmits<{
  'try-again': []
}>()
</script>

<style scoped>
.evaluation-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 24px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.result-title {
  font-size: 22px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  text-align: center;
}

.result-recognized {
  padding: 16px 20px;
  background: #f8fafc;
  border-radius: 12px;
}

.section-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.recognized-text {
  font-size: 18px;
  color: #475569;
  margin: 0;
  font-style: italic;
}

.btn-try-again {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 16px;
  background: #f1f5f9;
  color: #475569;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-try-again:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
}
</style>
