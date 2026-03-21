<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="logo">👋 Say Hi</span>
        <span class="badge">Admin</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          <span>📊</span> Dashboard
        </router-link>
        <router-link to="/users" class="nav-item">
          <span>👥</span> 用户管理
        </router-link>
        <router-link to="/practices" class="nav-item">
          <span>📚</span> 题目管理
        </router-link>
        <router-link to="/history" class="nav-item">
          <span>📈</span> 评估历史
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-email">{{ user?.email }}</span>
        </div>
        <button @click="logout" class="btn-logout">退出登录</button>
      </div>
    </aside>
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../composables/useAuth'

const { user, logout } = useAuth()
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: #1e293b;
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #334155;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.badge {
  background: #3b82f6;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #334155;
  color: white;
}

.nav-item.router-link-exact-active {
  background: #334155;
  color: white;
  border-left: 3px solid #3b82f6;
  padding-left: 17px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #334155;
}

.user-info {
  margin-bottom: 10px;
}

.user-email {
  font-size: 13px;
  color: #94a3b8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.btn-logout {
  width: 100%;
  padding: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  border: 1px solid #475569;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.main-content {
  flex: 1;
  background: #f8fafc;
  padding: 24px;
  overflow-y: auto;
}
</style>
