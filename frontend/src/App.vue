<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <router-link to="/" class="logo">
          <span class="logo-icon">👋</span>
          <span class="logo-text">Say Hi</span>
        </router-link>
        <nav class="header-nav" v-if="isAuthenticated">
          <router-link to="/" class="nav-link">📚 Practice</router-link>
          <router-link to="/history" class="nav-link">📊 History</router-link>
          <span class="nav-user">{{ user?.email }}</span>
          <button class="btn-logout" @click="logout">Logout</button>
        </nav>
        <div v-else class="header-nav">
          <router-link to="/login" class="nav-link">Log in</router-link>
        </div>
      </div>
    </header>

    <main class="app-main">
      <BrowserWarning />
      <router-view />
    </main>

    <footer class="app-footer">
      <p>Powered by OpenAI Whisper · Built with Vue.js &amp; FastAPI</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import BrowserWarning from './components/BrowserWarning.vue'
import { useAuth } from './composables/useAuth'

const { isAuthenticated, user, logout } = useAuth()
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: white;
  padding: 16px 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-content {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: white;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: white;
}

.nav-user {
  font-size: 13px;
  color: #94a3b8;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-logout {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.app-main {
  flex: 1;
  background: #f8fafc;
  padding-bottom: 40px;
}

.app-footer {
  padding: 20px 24px;
  text-align: center;
  background: #f1f5f9;
  border-top: 1px solid #e2e8f0;
}

.app-footer p {
  margin: 0;
  font-size: 13px;
  color: #94a3b8;
}

@media (max-width: 640px) {
  .nav-user {
    display: none;
  }
  .header-content {
    flex-wrap: wrap;
    gap: 8px;
  }
}
</style>