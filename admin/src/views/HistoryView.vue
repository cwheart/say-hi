<template>
  <div class="history-page">
    <h1>📈 评估历史</h1>
    <table class="data-table">
      <thead>
        <tr>
          <th>用户</th>
          <th>目标文本</th>
          <th>识别文本</th>
          <th>准确度</th>
          <th>完整度</th>
          <th>流畅度</th>
          <th>总分</th>
          <th>时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in history" :key="item.id">
          <td>{{ item.user_email || '-' }}</td>
          <td class="text-cell">{{ item.target_text }}</td>
          <td class="text-cell">{{ item.recognized_text }}</td>
          <td>{{ item.accuracy }}</td>
          <td>{{ item.completeness }}</td>
          <td>{{ item.fluency }}</td>
          <td><strong :style="{ color: getScoreColor(item.overall_score) }">{{ item.overall_score }}</strong></td>
          <td>{{ formatDate(item.created_at) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-if="!history.length && !loading" class="empty">暂无评估记录</div>
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page <= 1" @click="page--; fetchHistory()">上一页</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="page++; fetchHistory()">下一页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { getScoreColor } from '../types'
import type { AdminHistoryItem } from '../types'

const { getHistory } = useApi()

const history = ref<AdminHistoryItem[]>([])
const page = ref(1)
const totalPages = ref(1)
const loading = ref(false)

function formatDate(d: string) { return new Date(d).toLocaleString('zh-CN') }

async function fetchHistory() {
  loading.value = true
  try {
    const res = await getHistory(page.value, 20)
    history.value = res.items
    totalPages.value = res.total_pages
  } finally { loading.value = false }
}

onMounted(fetchHistory)
</script>

<style scoped>
.history-page h1 { margin-bottom: 20px; color: #1e293b; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.data-table th { text-align: left; padding: 12px 14px; font-size: 13px; color: #64748b; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 12px 14px; font-size: 14px; color: #334155; border-bottom: 1px solid #f1f5f9; }
.text-cell { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.empty { text-align: center; padding: 40px; color: #94a3b8; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; }
.pagination button { padding: 8px 16px; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
