<template>
  <div class="users-page">
    <h1>👥 用户管理</h1>
    <table class="data-table">
      <thead>
        <tr>
          <th>邮箱</th>
          <th>角色</th>
          <th>OpenID</th>
          <th>昵称</th>
          <th>状态</th>
          <th>注册时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.email || '-' }}</td>
          <td><span class="role-badge" :class="u.role">{{ u.role }}</span></td>
          <td class="text-cell">{{ u.openid || '-' }}</td>
          <td>{{ u.nickname || '-' }}</td>
          <td><span class="status-badge" :class="u.is_active ? 'active' : 'disabled'">{{ u.is_active ? '正常' : '已禁用' }}</span></td>
          <td>{{ formatDate(u.created_at) }}</td>
          <td>
            <button v-if="u.is_active" class="btn-sm btn-danger" @click="handleDisable(u.id)" :disabled="acting">禁用</button>
            <button v-else class="btn-sm btn-success" @click="handleEnable(u.id)" :disabled="acting">启用</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page <= 1" @click="page--; fetchUsers()">上一页</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="page++; fetchUsers()">下一页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import type { AdminUser } from '../types'

const { getUsers, disableUser, enableUser } = useApi()

const users = ref<AdminUser[]>([])
const page = ref(1)
const totalPages = ref(1)
const acting = ref(false)

function formatDate(d: string) { return new Date(d).toLocaleDateString('zh-CN') }

async function fetchUsers() {
  const res = await getUsers(page.value, 20)
  users.value = res.items
  totalPages.value = res.total_pages
}

async function handleDisable(id: string) {
  acting.value = true
  try { await disableUser(id); await fetchUsers() } finally { acting.value = false }
}

async function handleEnable(id: string) {
  acting.value = true
  try { await enableUser(id); await fetchUsers() } finally { acting.value = false }
}

onMounted(fetchUsers)
</script>

<style scoped>
.users-page h1 { margin-bottom: 20px; color: #1e293b; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.data-table th { text-align: left; padding: 12px 14px; font-size: 13px; color: #64748b; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 12px 14px; font-size: 14px; color: #334155; border-bottom: 1px solid #f1f5f9; }
.text-cell { max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 12px; }
.role-badge { font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.role-badge.admin { background: #dbeafe; color: #2563eb; }
.role-badge.user { background: #f1f5f9; color: #64748b; }
.status-badge { font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.status-badge.active { background: #dcfce7; color: #16a34a; }
.status-badge.disabled { background: #fee2e2; color: #dc2626; }
.btn-sm { padding: 4px 12px; font-size: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-danger:hover { background: #fecaca; }
.btn-success { background: #dcfce7; color: #16a34a; }
.btn-success:hover { background: #bbf7d0; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; }
.pagination button { padding: 8px 16px; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
