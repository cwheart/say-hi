<template>
  <div class="history-page">
    <div class="page-header">
      <h1>📊 Practice History</h1>
      <p class="subtitle">Review your past pronunciation evaluations</p>
    </div>

    <div v-if="loading" class="loading"><div class="spinner"></div><span>Loading...</span></div>

    <div v-else-if="errorMsg" class="error-state">❌ {{ errorMsg }}</div>

    <div v-else-if="history.length === 0" class="empty-state">
      <p>No practice history yet. Start practicing to see your results here!</p>
      <router-link to="/" class="btn-start">📚 Go to Practice Library</router-link>
    </div>

    <template v-else>
      <div class="history-list">
        <div v-for="item in history" :key="item.id" class="history-card">
          <div class="card-left">
            <div class="card-text">{{ item.target_text }}</div>
            <div class="card-meta">
              <span class="card-date">{{ formatDate(item.created_at) }}</span>
              <span v-if="item.practice_id" class="card-practice-id">{{ item.practice_id }}</span>
            </div>
          </div>
          <div class="card-right">
            <div class="card-score" :style="{ color: getScoreColor(item.overall_score) }">
              {{ item.overall_score }}
            </div>
            <div class="card-level">{{ getScoreLevel(item.overall_score) }}</div>
          </div>
        </div>
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button @click="changePage(page - 1)" :disabled="page <= 1" class="page-btn">← Prev</button>
        <span class="page-info">Page {{ page }} / {{ totalPages }}</span>
        <button @click="changePage(page + 1)" :disabled="page >= totalPages" class="page-btn">Next →</button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { getScoreColor, getScoreLevel } from '../types'
import type { HistoryItem } from '../types'

const { getHistory } = useApi()

const history = ref<HistoryItem[]>([])
const loading = ref(false)
const errorMsg = ref('')
const page = ref(1)
const totalPages = ref(0)

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

async function fetchHistory() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await getHistory(page.value, 10)
    history.value = res.items
    totalPages.value = res.total_pages
  } catch (err: any) {
    errorMsg.value = err.message || 'Failed to load history'
  } finally {
    loading.value = false
  }
}

function changePage(newPage: number) {
  page.value = newPage
  fetchHistory()
}

onMounted(() => fetchHistory())
</script>

<style scoped>
.history-page { max-width: 800px; margin: 0 auto; padding: 24px; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; font-weight: 800; color: #1e293b; margin: 0 0 8px; }
.subtitle { color: #64748b; font-size: 16px; margin: 0; }
.loading { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 48px; color: #64748b; }
.spinner { width: 24px; height: 24px; border: 3px solid #e2e8f0; border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-state { text-align: center; padding: 48px; color: #dc2626; }
.empty-state { text-align: center; padding: 48px; color: #94a3b8; }
.btn-start { display: inline-block; margin-top: 16px; padding: 10px 20px; background: #3b82f6; color: white; border-radius: 8px; text-decoration: none; font-weight: 600; }
.history-list { display: flex; flex-direction: column; gap: 12px; }
.history-card { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 12px; transition: box-shadow 0.2s; }
.history-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.card-left { flex: 1; min-width: 0; }
.card-text { font-size: 16px; font-weight: 600; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-meta { display: flex; gap: 12px; margin-top: 6px; font-size: 13px; color: #94a3b8; }
.card-practice-id { background: #f1f5f9; padding: 2px 8px; border-radius: 4px; }
.card-right { text-align: center; margin-left: 20px; flex-shrink: 0; }
.card-score { font-size: 32px; font-weight: 800; line-height: 1; }
.card-level { font-size: 12px; font-weight: 600; color: #94a3b8; margin-top: 4px; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 24px; }
.page-btn { padding: 8px 16px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; font-weight: 600; color: #475569; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-info { font-size: 14px; color: #64748b; }
</style>
