<template>
  <div class="practice-list">
    <div class="page-header">
      <h1>📚 Practice Library</h1>
      <p class="subtitle">Choose a word, phrase, or sentence to practice your pronunciation</p>
    </div>

    <!-- Filters -->
    <div class="filters">
      <div class="filter-group">
        <label>Category</label>
        <div class="filter-buttons">
          <button
            v-for="cat in categories"
            :key="cat.value"
            :class="['filter-btn', { active: selectedCategory === cat.value }]"
            @click="selectedCategory = selectedCategory === cat.value ? '' : cat.value"
          >
            {{ cat.icon }} {{ cat.label }}
          </button>
        </div>
      </div>
      <div class="filter-group">
        <label>Difficulty</label>
        <div class="filter-buttons">
          <button
            v-for="diff in difficulties"
            :key="diff.value"
            :class="['filter-btn', `diff-${diff.value}`, { active: selectedDifficulty === diff.value }]"
            @click="selectedDifficulty = selectedDifficulty === diff.value ? '' : diff.value"
          >
            {{ diff.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>Loading practices...</span>
    </div>

    <!-- Error -->
    <div v-else-if="errorMsg" class="error-state">
      <span>❌ {{ errorMsg }}</span>
      <button class="btn-retry" @click="fetchPractices">Retry</button>
    </div>

    <!-- Practice items -->
    <div v-else class="practice-grid">
      <router-link
        v-for="practice in practices"
        :key="practice.id"
        :to="`/practice/${practice.id}`"
        class="practice-card"
      >
        <div class="card-category">
          {{ getCategoryIcon(practice.category) }} {{ practice.category }}
        </div>
        <div class="card-text">{{ practice.text }}</div>
        <div class="card-footer">
          <span :class="['difficulty-badge', `diff-${practice.difficulty}`]">
            {{ practice.difficulty }}
          </span>
          <span v-if="practice.hint" class="hint-indicator" title="Has pronunciation hint">💡</span>
        </div>
      </router-link>
    </div>

    <!-- Empty state -->
    <div v-if="!loading && !errorMsg && practices.length === 0" class="empty-state">
      <span>No practices found. Try changing the filters.</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import type { Practice } from '../types'

const { getPractices } = useApi()

const practices = ref<Practice[]>([])
const loading = ref(false)
const errorMsg = ref('')
const selectedCategory = ref('')
const selectedDifficulty = ref('')

const categories = [
  { value: 'word', label: 'Words', icon: '🔤' },
  { value: 'phrase', label: 'Phrases', icon: '💬' },
  { value: 'sentence', label: 'Sentences', icon: '📝' },
]

const difficulties = [
  { value: 'beginner', label: '⭐ Beginner' },
  { value: 'intermediate', label: '⭐⭐ Intermediate' },
  { value: 'advanced', label: '⭐⭐⭐ Advanced' },
]

function getCategoryIcon(category: string): string {
  const map: Record<string, string> = { word: '🔤', phrase: '💬', sentence: '📝' }
  return map[category] || '📄'
}

async function fetchPractices() {
  loading.value = true
  errorMsg.value = ''
  try {
    const response = await getPractices(
      selectedCategory.value || undefined,
      selectedDifficulty.value || undefined,
    )
    practices.value = response.items
  } catch (err: any) {
    errorMsg.value = err.message || 'Failed to load practices'
  } finally {
    loading.value = false
  }
}

watch([selectedCategory, selectedDifficulty], () => {
  fetchPractices()
})

onMounted(() => {
  fetchPractices()
})
</script>

<style scoped>
.practice-list {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #64748b;
  font-size: 16px;
  margin: 0;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
}

.filter-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.filter-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #94a3b8;
}

.filter-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
}

.btn-retry {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.practice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.practice-card {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  cursor: pointer;
}

.practice-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  transform: translateY(-2px);
}

.card-category {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: #94a3b8;
  margin-bottom: 8px;
}

.card-text {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
  flex: 1;
  margin-bottom: 12px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.difficulty-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: capitalize;
}

.diff-beginner {
  background: #dcfce7;
  color: #16a34a;
}

.diff-intermediate {
  background: #fef3c7;
  color: #d97706;
}

.diff-advanced {
  background: #fee2e2;
  color: #dc2626;
}

.hint-indicator {
  font-size: 16px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #94a3b8;
  font-size: 16px;
}

@media (max-width: 640px) {
  .practice-grid {
    grid-template-columns: 1fr;
  }
  .filters {
    padding: 16px;
  }
}
</style>
