<template>
  <div class="dashboard">
    <h1>📊 Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ userCount }}</div>
        <div class="stat-label">用户总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ practiceCount }}</div>
        <div class="stat-label">练习题目</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ historyCount }}</div>
        <div class="stat-label">评估记录</div>
      </div>
    </div>

    <div class="section" v-if="recentHistory.length">
      <h2>最近评估</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>用户</th>
            <th>目标文本</th>
            <th>得分</th>
            <th>时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in recentHistory" :key="item.id">
            <td>{{ item.user_email || '-' }}</td>
            <td class="text-cell">{{ item.target_text }}</td>
            <td><span class="score" :style="{ color: getScoreColor(item.overall_score) }">{{ item.overall_score }}</span></td>
            <td>{{ formatDate(item.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import { getScoreColor } from '../types'
import type { AdminHistoryItem } from '../types'

const { getUsers, getPractices, getHistory } = useApi()

const userCount = ref(0)
const practiceCount = ref(0)
const historyCount = ref(0)
const recentHistory = ref<AdminHistoryItem[]>([])

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  try {
    const [usersRes, practicesRes, historyRes] = await Promise.all([
      getUsers(1, 1),
      getPractices(),
      getHistory(1, 5),
    ])
    userCount.value = usersRes.total
    practiceCount.value = practicesRes.total
    historyCount.value = historyRes.total
    recentHistory.value = historyRes.items
  } catch (e) {
    console.error('Failed to load dashboard data', e)
  }
})
</script>

<style scoped>
.dashboard h1 { margin-bottom: 24px; color: #1e293b; }
.dashboard h2 { margin-bottom: 16px; color: #334155; font-size: 18px; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  text-align: center;
}

.stat-value { font-size: 32px; font-weight: 700; color: #3b82f6; }
.stat-label { font-size: 14px; color: #64748b; margin-top: 4px; }

.section { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

.data-table { width: 100%; border-collapse: collapse; }
.data-table th { text-align: left; padding: 10px 12px; font-size: 13px; color: #64748b; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 10px 12px; font-size: 14px; color: #334155; border-bottom: 1px solid #f1f5f9; }
.text-cell { max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.score { font-weight: 700; }
</style>
