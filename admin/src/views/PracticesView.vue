<template>
  <div class="practices-page">
    <div class="page-header">
      <h1>📚 题目管理</h1>
      <button class="btn-primary" @click="$router.push('/practices/new')">+ 新建题目</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>文本</th>
          <th>分类</th>
          <th>难度</th>
          <th>提示</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in practices" :key="p.id">
          <td class="id-cell">{{ p.id }}</td>
          <td>{{ p.text }}</td>
          <td><span class="cat-badge">{{ p.category }}</span></td>
          <td><span class="diff-badge" :class="p.difficulty">{{ p.difficulty }}</span></td>
          <td class="text-cell">{{ p.hint || '-' }}</td>
          <td class="actions">
            <button class="btn-sm btn-edit" @click="$router.push(`/practices/${p.id}/edit`)">编辑</button>
            <button class="btn-sm btn-danger" @click="handleDelete(p.id)" :disabled="deleting">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import type { Practice } from '../types'

const { getPractices, deletePractice } = useApi()

const practices = ref<Practice[]>([])
const deleting = ref(false)

async function fetchPractices() {
  const res = await getPractices()
  practices.value = res.items
}

async function handleDelete(id: string) {
  if (!confirm('确定删除此题目？')) return
  deleting.value = true
  try { await deletePractice(id); await fetchPractices() } finally { deleting.value = false }
}

onMounted(fetchPractices)
</script>

<style scoped>
.practices-page h1 { color: #1e293b; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.btn-primary { padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { background: #2563eb; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.data-table th { text-align: left; padding: 12px 14px; font-size: 13px; color: #64748b; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 12px 14px; font-size: 14px; color: #334155; border-bottom: 1px solid #f1f5f9; }
.id-cell { font-family: monospace; font-size: 12px; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.text-cell { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cat-badge { font-size: 12px; padding: 2px 8px; background: #e0f2fe; color: #0369a1; border-radius: 10px; font-weight: 600; }
.diff-badge { font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.diff-badge.beginner { background: #dcfce7; color: #16a34a; }
.diff-badge.intermediate { background: #fef3c7; color: #d97706; }
.diff-badge.advanced { background: #fee2e2; color: #dc2626; }
.actions { display: flex; gap: 6px; }
.btn-sm { padding: 4px 12px; font-size: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-edit { background: #e0f2fe; color: #0369a1; }
.btn-edit:hover { background: #bae6fd; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-danger:hover { background: #fecaca; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
