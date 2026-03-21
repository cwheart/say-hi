<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>🚀 Create Account</h1>
      <p class="subtitle">Start practicing your English pronunciation</p>

      <div v-if="errorMsg" class="error-banner">{{ errorMsg }}</div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="Min 6 characters" required minlength="6" />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Repeat password" required />
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading" class="spinner-sm"></span>
          {{ loading ? 'Creating...' : 'Sign Up' }}
        </button>
      </form>

      <p class="auth-switch">
        Already have an account? <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { register } = useAuth()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const loading = ref(false)

async function handleRegister() {
  errorMsg.value = ''

  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    errorMsg.value = 'Password must be at least 6 characters'
    return
  }

  loading.value = true
  try {
    await register({ email: email.value, password: password.value })
    router.push('/')
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 160px); padding: 24px; }
.auth-card { width: 100%; max-width: 400px; background: white; border-radius: 16px; padding: 40px 32px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
.auth-card h1 { font-size: 28px; font-weight: 800; color: #1e293b; margin: 0 0 8px; text-align: center; }
.subtitle { text-align: center; color: #64748b; margin: 0 0 24px; }
.error-banner { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 8px; font-size: 14px; margin-bottom: 16px; }
.auth-form { display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 14px; font-weight: 600; color: #475569; }
.form-group input { padding: 12px 14px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 16px; transition: border-color 0.2s; }
.form-group input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.btn-submit { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px; background: #3b82f6; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
.btn-submit:hover:not(:disabled) { background: #2563eb; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
.spinner-sm { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.auth-switch { text-align: center; margin-top: 20px; font-size: 14px; color: #64748b; }
.auth-switch a { color: #3b82f6; font-weight: 600; }
</style>
