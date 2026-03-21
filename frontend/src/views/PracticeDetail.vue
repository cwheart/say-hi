<template>
  <div class="practice-detail">
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>Loading...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="errorMsg" class="error-state">
      <span>❌ {{ errorMsg }}</span>
      <router-link to="/" class="btn-back">← Back to List</router-link>
    </div>

    <!-- Practice content -->
    <template v-else-if="practice">
      <div class="detail-header">
        <router-link to="/" class="back-link">← Back to Library</router-link>
        <div class="detail-meta">
          <span :class="['difficulty-badge', `diff-${practice.difficulty}`]">
            {{ practice.difficulty }}
          </span>
          <span class="category-badge">{{ practice.category }}</span>
        </div>
      </div>

      <!-- Target text -->
      <div class="target-section">
        <label class="section-label">Say this:</label>
        <div class="target-text">{{ practice.text }}</div>
        <div v-if="practice.hint" class="hint">
          💡 Hint: {{ practice.hint }}
        </div>
        <div v-if="bestScore !== null" class="best-score">
          🏆 Your best score: <strong :style="{ color: getScoreColor(bestScore) }">{{ bestScore }}</strong>
        </div>
      </div>

      <!-- Audio recorder -->
      <AudioRecorder ref="recorderRef" />

      <!-- Submit button -->
      <button
        class="btn-submit"
        :disabled="!canSubmit"
        @click="submitEvaluation"
      >
        <template v-if="evaluating">
          <span class="spinner-sm"></span>
          Analyzing your pronunciation...
        </template>
        <template v-else>
          🚀 Submit for Evaluation
        </template>
      </button>

      <!-- Evaluation result -->
      <EvaluationResultComponent
        v-if="evaluationResult"
        :result="evaluationResult"
        @try-again="handleTryAgain"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '../composables/useApi'
import type { Practice, EvaluationResult } from '../types'
import { getScoreColor } from '../types'
import AudioRecorder from '../components/AudioRecorder.vue'
import EvaluationResultComponent from '../components/EvaluationResult.vue'

const route = useRoute()
const { getPracticeById, evaluatePronunciation, getBestScore } = useApi()

const practice = ref<Practice | null>(null)
const loading = ref(false)
const errorMsg = ref('')
const evaluating = ref(false)
const evaluationResult = ref<EvaluationResult | null>(null)
const recorderRef = ref<InstanceType<typeof AudioRecorder> | null>(null)
const bestScore = ref<number | null>(null)

const canSubmit = computed(() => {
  return (
    recorderRef.value?.state === 'recorded' &&
    recorderRef.value?.audioBlob &&
    !evaluating.value
  )
})

async function fetchPractice() {
  const id = route.params.id as string
  loading.value = true
  errorMsg.value = ''
  try {
    practice.value = await getPracticeById(id)
    bestScore.value = await getBestScore(id)
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Practice not found'
  } finally {
    loading.value = false
  }
}

async function submitEvaluation() {
  if (!practice.value || !recorderRef.value?.audioBlob) return

  evaluating.value = true
  evaluationResult.value = null

  try {
    const result = await evaluatePronunciation(
      recorderRef.value.audioBlob,
      practice.value.text,
      practice.value.id,
    )
    evaluationResult.value = result
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Evaluation failed. Please try again.'
  } finally {
    evaluating.value = false
  }
}

function handleTryAgain() {
  evaluationResult.value = null
  recorderRef.value?.resetRecording()
}

onMounted(() => {
  fetchPractice()
})
</script>

<style scoped>
.practice-detail {
  max-width: 700px;
  margin: 0 auto;
  padding: 24px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #64748b;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-sm {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px;
}

.btn-back {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border-radius: 8px;
  text-decoration: none;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.back-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

.detail-meta {
  display: flex;
  gap: 8px;
}

.difficulty-badge,
.category-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: capitalize;
}

.category-badge {
  background: #e0f2fe;
  color: #0284c7;
}

.diff-beginner { background: #dcfce7; color: #16a34a; }
.diff-intermediate { background: #fef3c7; color: #d97706; }
.diff-advanced { background: #fee2e2; color: #dc2626; }

.target-section {
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
}

.section-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.target-text {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.4;
}

.hint {
  margin-top: 12px;
  padding: 10px 14px;
  background: #fffbeb;
  border-radius: 8px;
  color: #92400e;
  font-size: 14px;
}

.btn-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 16px;
  margin-top: 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
